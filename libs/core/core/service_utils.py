from json import loads, dumps
from random import randint
from time import time, sleep
import os
import allure
import datetime
import logging
import requests
from allure.constants import AttachmentType

from libs.core.core.data import FormattedEncoder, SimpleEncoder
from libs.core.core.logger import logger
from libs.core.core.step import step
from libs.core.core import COVERAGE_FOLDER
import re
import inspect
import uuid

CONTENT_TYPE_JSON_RPC = 'application/json-rpc'
START_WAITING_INTERVAL = 0.1
REPLICATION_LAG_INCREASING_FACTOR = 2
ids = {}


def to_curl(response):
    req = response.request
    command = 'curl -X {method} -H {headers} {data} "{uri}"'

    data = ''
    if req.body:
        data = " -d '%s'" % req.body

    headers = ['"{0}: {1}"'.format(k, v)
               for k, v in req.headers.items()
               if k.lower() != 'content-length']
    headers = ' -H '.join(headers)
    return command.format(method=req.method, headers=headers, data=data, uri=req.url)


@step('Send request to service')
def send_request(url, method='GET', headers=None, params=None, json=None, verify=True):
    response = send_raw_request(url=url, method=method, headers=headers, params=params, json=json, verify=verify)

    if _suspect_json(response):
        return response.status_code, response.json()
    return response.status_code, response.text


def send_raw_request(url, method='GET', headers=None, params=None, cert=None, json=None, timeout=None, auth=None,
                     cookies=None, allow_redirects=True, verify=True, session=None, response_encoding="utf-8"):
    """
    common method to send get and post requests
    :param url:
    :param method:
    :param headers:
    :param params:
    :param json:
    :param session: optional requests.Session object
    :return: requests.Response object

    """
    data = None

    _process_data_for_coverage_report(json, headers, method, url)

    if not timeout:
        timeout = 120
    if not headers:
        headers = {}
    if json is not None:
        headers.setdefault('Content-Type', 'application/json')
        data = dumps(json, cls=SimpleEncoder)

    with step(u"Send request to \nURL:%s" % url):
        logger.info(u'Send raw request:\n{hr}\n'
                    u'Method: {method} \n'
                    u'URL: {url}:\n'
                    u'Headers: {headers}\n'
                    u'Certificate: {cert}\n'
                    u'Params: {params}\n'
                    u'Body: {json}\n{hr}'.format(method=method, url=url,
                                                 headers=dumps(headers, cls=FormattedEncoder),
                                                 cert=str(cert), params=params,
                                                 json=dumps(json, cls=FormattedEncoder), hr='-' * 100))

        provider = requests
        if isinstance(session, requests.Session):
            provider = session
        response = provider.request(method=method, url=url, headers=headers, params=params,
                                    data=data, cert=cert, timeout=timeout, auth=auth, cookies=cookies,
                                    allow_redirects=allow_redirects, verify=verify)

        # A dirty hack, preventing encoding guessing using chardet
        # See http://docs.python-requests.org/en/master/api/#requests.Response.text
        # chardet is dramatically slow on large responses, and our GO API always use utf-8
        if not response.encoding:
            response.encoding = response_encoding

        logger.info(u'Equivalent "%s"' % to_curl(response))
        if 'image' not in response.headers.get('Content-Type', []) and \
           'bytes' not in response.headers.get('Accept-Ranges', []):
            _attach_to_report(response)
    return response


def _attach_to_report(response):
    with step(("Get response code: %s" % response.status_code)):

        if logger.isEnabledFor(logging.INFO):
            logger.info(u'Received response:\n{br}\n'
                        u'Status: {status}\n'
                        u'Headers: {headers}\n'
                        u'Body: {body}\n{br}\n'.format(status=response.status_code,
                                                       headers=dumps(dict(response.headers), cls=FormattedEncoder),
                                                       body=_format_data(response.text),
                                                       br='=' * 100))
        try:
            allure.attach('request', response.url, type=AttachmentType.TEXT)
            if response.request.method == 'POST' and \
                    _suspect_json(response.request):
                allure.attach('request body',
                              _format_data(response.request.body),
                              type=AttachmentType.JSON)
            allure.attach('response headers', dumps(dict(response.headers), indent=4, sort_keys=True),
                          type=AttachmentType.TEXT)
            if _suspect_json(response):
                allure.attach('response', dumps(response.json(), indent=4, sort_keys=True),
                              type=AttachmentType.JSON)
            else:
                allure.attach('response', dumps(response.text), type=AttachmentType.HTML)
        except AttributeError:
            logger.info(u"\n\nWe don't attach files during test collection phase\n")
        except ValueError:
            logger.info(u"\n\nWe cannot attach the file as json, it was not a json\n")


def _format_data(data):
    try:
        return dumps(loads(data), cls=FormattedEncoder)
    except ValueError:
        return data


def _suspect_json(response):
    content_type = response.headers.get('Content-Type', [])
    return ('application/json' in content_type) or (CONTENT_TYPE_JSON_RPC in content_type)


def _get_data_from_json_rpc(url, json):
    """
    Prepare data from rpc request to handlers coverage format for future parsing
    """
    match = re.search('(.*\/\/.*?)\/', url)
    if match and len(match.groups()) > 0:
        url = '{}{}'.format(match.group(1), json.get('method'))
        method = 'POST'
        _save_trace(method, url)


def _process_data_for_coverage_report(json, headers, method, url):
    """
    Function detect rpc or regular request and call appropriate functions for processing
    """
    if headers \
            and 'Content-Type' in headers \
            and CONTENT_TYPE_JSON_RPC in headers.get('Content-Type', []):
        _get_data_from_json_rpc(url, json)
    else:
        _save_trace(method, url)


def _save_trace(method, url):
    """
    Function for saving information about request:
    We save method, url and function which call send_raw_request function
    This information is needed for handlers coverage report
    """
    frame = inspect.stack()
    frame_element = 0
    keep_read_frames = True
    save = None

    # Keep reading frame untill we not find _pytest/python.py or reach 30 frame, then save frame - 1
    # Frame before the frame with  _pytest/python.py contains the information that we need
    # (filename, funciton, line num)
    # In 95% cases we will not reach frame 30 - this number was obtained empirical way
    while keep_read_frames and (frame_element < 30 and frame_element <= len(frame) - 1):
        if frame[frame_element][1] and '_pytest/python.py' in frame[frame_element][1]:
            keep_read_frames = False
            save = frame[frame_element - 1]
        frame_element += 1
    if save is not None and len(save) > 1:
        file_name = re.sub(r'.*/tests/', '', save[1])
        line = dumps(
            dict(method=method, url_name=url, file_name=file_name, line_num=save[2], function_name=save[3])) + "\n"
        log_dir = os.path.normpath(
            os.path.abspath(os.path.expanduser(os.path.expandvars(COVERAGE_FOLDER)))) + '/'
        object_id = id(save[0])

        # Generate uniq id for each test, we need it to save each test requests(function) in uniq file
        # (instead of creating uniq file for each request)
        if object_id in ids:
            uniq_id = ids[object_id]
        else:
            uniq_id = uuid.uuid4()
            ids[object_id] = uniq_id

        log_file = log_dir + '/' + str(uniq_id) + '.txt'
        log_dir = os.path.abspath(os.path.dirname(log_file))

        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        with open(log_file, 'a') as log:
            log.write(line)


class Retry(object):
    """
    Object for retry sending request and check response until it will be expected.
    If no response is expected after specific timeout, raise an exception.
    """
    def __init__(self, sender, checker, timeout=10):
        """
        :param sender: sender - callable object for sending request to the handler
            sendr tuple - (sender_func, sender_args[], sender_kwargs{})
        :param checker: checker - callable object for checking response from handler
            tuple - (checker_func, checker_args[], checker_kwargs{})
        :param timeout: time for waiting replication lag
            Replictaion lag timeout SLA should be in the config, in beautiful future
            But now - just pass it in the constructor or use default
        """
        self.sender = sender
        self.checker = checker
        self.timeout = float(timeout)

    def __call__(self):
        """
        :return: response_code and response or raise exception
        """
        sender_func, sender_args, sender_kwargs = self.sender
        checker_func, checker_args, checker_kwargs = self.checker
        start_time = time()
        interval = START_WAITING_INTERVAL
        self._attempt = 0

        with step('Wait expected response for {} sec'.format(self.timeout)):
            while time() - start_time < self.timeout:
                self._attempt += 1
                if not checker_func or not callable(checker_func):
                    return sender_func(*sender_args, **sender_kwargs)
                with step('Attempt #{}'.format(self._attempt)):
                    try:
                        with step('Send request to target handler'):
                            code, response = sender_func(*sender_args, **sender_kwargs)
                            checker_kwargs['code'] = code
                            checker_kwargs['response'] = response
                        with step('Validate response from target handler'):
                            checker_func(*checker_args, **checker_kwargs)
                            return code, response
                    except Exception as e:
                        logger.exception(e)
                        sleep(interval)
                        interval *= REPLICATION_LAG_INCREASING_FACTOR
            raise RetryMaxCountExceeded('Max attempts: [{0}], time ellapses: [{1}] sec'.
                                        format(self._attempt, time() - start_time))


class RetryMaxCountExceeded(Exception):
    """ Retry attempts exceeded error. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

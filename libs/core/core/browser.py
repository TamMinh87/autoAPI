import json

import allure
from allure.constants import AttachmentType
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from libs.core.core import logger
from libs.core.core.step import step


class BrowserRunner(object):
    def __init__(self):
        self.local_browsers = {'phantomjs': webdriver.PhantomJS,
                               'firefox': webdriver.Firefox,
                               'chrome': webdriver.Chrome}

        self.browser = None

    def _start_local(self, browser_name, mobile, opera_mini, user_agent):
        browser_cap = self.local_browsers.get(browser_name)
        if not browser_cap:
            raise Exception('No capabilities found for %s. Please use one of %s' % (
                browser_name, ', '.join(self.local_browsers.keys())))
        if browser_name == 'chrome':
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-setuid-sandbox")
            # https://bugs.chromium.org/p/chromedriver/issues/detail?id=817
            chrome_options.add_argument('--dns-prefetch-disable')

            if mobile:
                if opera_mini:
                    mobile_emulation = {"deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
                                        "userAgent": 'Opera/9.80 (J2ME/MIDP; Opera Mini/9.80 (S60; SymbOS; '
                                                     'Opera Mobi/23.348; U; en) Presto/2.5.25 Version/10.54'}
                else:
                    mobile_emulation = {"deviceName": "Samsung Galaxy Note II"}

                chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
            else:
                if user_agent:
                    chrome_options.add_argument('user-agent={}'.format(user_agent))

            self.browser = browser_cap(desired_capabilities=chrome_options.to_capabilities())
        else:
            self.browser = browser_cap()
        self.browser.maximize_window()

    @step('start browser')
    def start(self, browser_name='phantomjs', mobile=False, opera_mini=False, user_agent=None):
        if self.is_running():
            return self.browser

        self._start_local(browser_name, mobile, opera_mini, user_agent)

    def attach_artifacts(self, artifact_name=''):
        if self.browser:
            try:
                allure.attach('{} screenshot'.format(artifact_name),
                              self.browser.get_screenshot_as_png(),
                              type=AttachmentType.PNG)
                for log_type in self.browser.log_types:
                    allure.attach('{} {} log'.format(artifact_name, log_type),
                                  json.dumps(self.browser.get_log(log_type), indent=4, sort_keys=True),
                                  type=AttachmentType.TEXT)
                allure.attach('{} html'.format(artifact_name),
                              self.browser.page_source,
                              type=AttachmentType.HTML)
                allure.attach('{} cookies'.format(artifact_name),
                              json.dumps(self.browser.get_cookies(), indent=4, sort_keys=True),
                              type=AttachmentType.TEXT)
                allure.attach('{} url'.format(artifact_name),
                              self.browser.current_url,
                              type=AttachmentType.TEXT)
                allure.attach('{} application cache status'.format(artifact_name),
                              json.dumps(self.browser.application_cache.status, indent=4, sort_keys=True),
                              type=AttachmentType.TEXT)
            except Exception as e:
                logger.error('cannot save artifacts %s' % e)

    @step('stop browser')
    def stop(self):
        if self.browser:
            self.browser.quit()
            self.browser = None

    def is_running(self):
        return bool(self.browser)

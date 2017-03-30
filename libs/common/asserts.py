import traceback
# assert_that re-declared below with calling original function
from hamcrest import *
from libs.common.converters import typify, unicodify

# Original version of assert that will be monkey patched for safe encoding conversion
original_assert_that = assert_that
# Deferred asserts bundle
deferred = list()


def defer(do, *args, **kwargs):
    """ Collects and defer till teardown all raised asserts """

    global deferred
    try:
        do(*args, **kwargs)
    except AssertionError as e:
        source_file, line, item, callee = traceback.extract_stack()[-2]
        deferred.append({
            'file': source_file,
            'line': line,
            'callee': callee,
            'message': e.__str__()
            # if len(e.__str__()) < 500
            # else '{} ... [cropped]'.format(e.__str__()[:500])
        })
    return deferred


def assert_deferred(*args, **kwargs):
    """ Collects and defer till teardown all raised asserts """

    return defer(assert_that, *args, **kwargs)


def raise_deferred(items=deferred):
    """ Raise all deferred assert with formatted output"""

    data = ['{}\n# {} - {}'
            .format('-' * 50, index + 1, item.get('message'))
            for index, item in enumerate(items)]
    if data:
        raise AssertionError('Deferred asserts raised\n{}'.format('\n'.join(data)))


def typify_assert_object(data, cast=unicodify):
    """ Typify matcher object value """
    return data


def assert_that(*args, **kwargs):
    """ [MonkeyPatch] Cast arguments type to appropriate with context """

    return original_assert_that(*typify_assert_object(typify(args, cast=unicodify)),
                                **typify_assert_object(typify(kwargs, cast=unicodify)))

import allure
import pytest

from allure.constants import AttachmentType
from config.config_reader import config_common, update_config_by_environment
from libs.core.core.logger import logger_stream, setLogLevel

option_list = (
    'db_password', 'db_user', 'db_name', 'twitch_api_url'
)


def pytest_addoption(parser):
    parser.addoption('--env', action='store', default='local')
    for option in option_list:
        parser.addoption('--%s' % option, action='store', default=None)


def set_options(config, option_list, section='DEFAULT'):
    for option in option_list:
        value = config.getoption('--%s' % option)
        if value:
            config_common.set(section, option, value)


def pytest_configure(config):
    update_config_by_environment(config_common, config.getoption("--env"))

    set_options(config, option_list)
    # set log level
    setLogLevel(config_common.get("DEFAULT", "log_level"))

    # just show properties in allure report
    deprecated = [k for k, _ in config_common.items('DEFAULT') if ('password' in k or 'secret' in k)]
    data = {name: value for name, value in config_common.items('DEFAULT') if name not in deprecated}
    allure.environment(**data)


@pytest.fixture(scope='function', autouse=True)
def attach(request):
    def fin():
        allure.attach('log', logger_stream.getvalue(), type=AttachmentType.TEXT)
        logger_stream.truncate(0)
        logger_stream.seek(0)

    request.addfinalizer(fin)

from os.path import abspath, dirname, exists
from configparser import ConfigParser, ExtendedInterpolation

CONFIGS = {
    uid: '{}/{}'.format(dirname(abspath(__file__)), file_name)
    for uid, file_name in dict(
        API='config_common.ini',
        ENV='env.ini'
    ).items()
}


def get_config(config_uid):
    """Function returns one of the configs
    :param config_uid: API, GUI, ES or ENV value to read selected config
    :return: config

    """
    if not exists(CONFIGS[config_uid]):
        raise AssertionError('Configuration file does n\'t exists: {}'
                             .format(CONFIGS[config_uid]))
    config = ConfigParser(interpolation=ExtendedInterpolation(), allow_no_value=True)
    config.read(CONFIGS[config_uid])
    return config


def update_config_by_environment(config, env=None):
    """Function updates selected config default values with values from environment config
    :param config - ConfigParser instance to update
    :param env - string; environment section key to get values from env config

    """
    if env is not None:
        config.set('DEFAULT', 'environment', env)

    config_env = get_config('ENV')
    data = dict(config_env.items(config.get('DEFAULT', 'environment')))
    config.read_dict(dict(DEFAULT=data))


def _init_common_config():
    """Method returns API config patched with data from ENV config with default environment"""

    config_api = get_config('API')
    update_config_by_environment(config_api)
    return config_api

config_common = _init_common_config()

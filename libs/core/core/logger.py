# -*- coding: utf-8 -*-
import sys
import logging

from io import StringIO


logger = logging.getLogger('ftest')
logger.setLevel(logging.DEBUG)

logger_stream = StringIO()

# create console handlers with custom stream and sys.out
console_handler_custom = logging.StreamHandler(stream=logger_stream)
console_handler_standard = logging.StreamHandler(stream=sys.stdout)
console_handler_custom.setLevel(logging.DEBUG)
console_handler_standard.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler_custom.setFormatter(formatter)
console_handler_standard.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(console_handler_custom)
logger.addHandler(console_handler_standard)


def setLogLevel(level):
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: {}".format(level))
    logger.setLevel(numeric_level)

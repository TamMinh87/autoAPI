import calendar
import datetime
import random
import string
import unicodedata
from datetime import date
from datetime import timedelta

from faker import Faker

from libs.common.converters import md5_digest, unicodify

fake = Faker()


def get_random_word():
    return fake.word()


def get_random_name():
    return '%s %s %s' % (get_random_word(), " ", get_random_word())


def get_random_numbers():
    return str(fake.unix_time())


def get_random_number_by_range(start=0, end=9999999):
    return random.randint(start, end)

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


def get_random_email():
    """
    Function is used because each its calling generates
    unique email as compared with variable using.
    """
    email = '%s_%s_%s@%s' % (fake.first_name(), fake.last_name(), str(fake.unix_time()), fake.free_email_domain())
    #  need to replace ' sign from last_name and first_name
    return email.replace('\'', '')


def get_random_first_name():
    return fake.first_name()


def get_random_last_name():
    return fake.last_name()


def get_random_password():
    return '%s%s' % (str(fake.unix_time()), get_random_first_name())


def get_random_full_name():
    return fake.name()


def get_random_date():
    return fake.date()


def get_random_ipv4():
    return fake.ipv4()


def get_random_uri():
    return fake.uri()


def get_random_word():
    return fake.word()


def get_unique_word():
    word = '%s_%s' % (fake.word(), str(fake.unix_time()))
    return word


def get_random_address():
    return fake.address()


def get_random_phone_number():
    return fake.phone_number()


def get_random_city():
    return fake.city()


def get_random_numbers():
    return str(fake.unix_time())


def get_random_postcode():
    return fake.postcode()


def get_random_country_code():
    return fake.country_code()


def get_random_date_time_as_string(format='%Y-%m-%d %m:%S:%S'):
    return fake.date_time().strftime(format)


def get_random_numeral_except_one():
    return random.randint(2, 9)


def get_random_date_before_today():
    return get_random_datetime_before_today().strftime('%Y-%m-%d %m:%S:%S')


def get_random_datetime_before_today():
    return fake.date_time_between(start_date="-35y", end_date="now")


def get_random_date_after_today(format='%Y-%m-%d %m:%S:%S'):
    return get_random_datetime_after_today().strftime(format)


def get_random_datetime_after_today():
    return fake.date_time_between(start_date="now", end_date="+35y")


def get_random_cookie():
    return fake.sha1()


def get_random_status():
    return random.choice(['active',
                          'inactive',
                          'deleted'])


def get_random_boolean():
    return random.choice([True,
                          False])


# Strings
def get_random_string(length=random.randint(3, 10)):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def get_random_hash():
    return md5_digest(get_random_string(100))


# Date
def add_date(date=datetime.datetime.today(), days=0, months=0, years=0, date_format='%Y-%m-%d'):
    """
    :param date: instanse of datetime.datetime
    :param days: +/- number of days
    :param months: +/- number of months
    :param years: +/- number of years
    :param date_format: date format
    :return: date in future or in past
    """
    weeks = months * 4 + years * 52
    """
    months*4 - 4 weeks per month
    years*52 - 52 weeks per year
    """
    return (date + timedelta(days=days, weeks=weeks)).strftime(date_format)


def get_random_specsymbols(length=random.randint(3, 10)):
    return ''.join(random.choice(string.punctuation) for _ in range(length))


def get_random_number_from_range(start=0, end=1000000000000000):
    return random.randint(start, end)


def get_random_latitude():
    return round(random.uniform(-90.0, 90.0), 5)


def get_random_longitude():
    return round(random.uniform(-180.0, 180.0), 5)


def get_random_float(precision=5):
    return round(random.random() * random.randint(1, 1000), precision)


def get_random_promotion_name():
    return '%s %s %s' % (get_random_word(), str(fake.unix_time()), get_random_word())


def get_random_promotion_description():
    return fake.sentence()


def get_random_password_static():
    # Static vars are needed to not generate new data when each calling is done,
    # e.g. for password changing and keep old value in memory

    random_password_static = '%s%s' % (str(fake.unix_time()), get_random_first_name())
    #  need to replace ' sign from last_name and first_name
    random_password_static = random_password_static.replace('\'', '')
    return random_password_static


get_random_email_static = '%s_%s_%s@%s' % (fake.first_name(), fake.last_name(), str(fake.unix_time()),
                                           fake.free_email_domain())


def get_random_list_element(list_of_elements):
    if list_of_elements and (isinstance(list_of_elements, list) or isinstance(list_of_elements, tuple)):
        return random.choice(list_of_elements)
    return []


def get_number_from_string_number(level):
    levels_structure = dict(first=1, second=2, third=3, fourth=4, fifth=5)
    return levels_structure.get(level)


def get_weekday_days_cart_rule_english(days=0):
    return calendar.day_name[(date.today() + timedelta(days=days)).weekday()]


def get_random_unique_text_field(field_name=''):
    return field_name + "_" + str(datetime.time()) + "_" + str(random.random())


def get_fast_delivery_location(location):
    params = dict()
    for key, value in location.items():
        if key.lower() == "postcode":
            params["zipcode"] = str(value)
        if key.lower() == "region":
            params["region_id"] = value
        if key.lower() in ("area", "district"):
            params["subdistrict_id"] = value
        if key.lower() == "city":
            params["city_id"] = value
    return params


def get_random_utf8_string(length=random.randint(1, 15)):
    ustr = ''
    # 'LMNPSZ' is general categories (letter, mark, number, punctuation, separator
    # ftp://ftp.unicode.org/Public/3.0-Update/UnicodeData-3.0.0.html#General Category
    group = 'LNPSZ'
    if length > 1:
        group += 'M'  # want to generate at least one whole symbol, not only mark
    while len(ustr) < length:
        code = random.randint(256, 65535)
        if unicodedata.category(chr(code))[0] in (group):
            ustr += chr(code)

    return unicodify(ustr)


def get_random_config_sku():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))


def get_random_simple_sku(config_sku=None):
    config_sku = config_sku or get_random_config_sku()
    return '%s-%s' % (config_sku, random.randint(1, 1000000))


def get_logging_id(url):
    return 'test_%s_%s' % (url, datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f"))


def next_from(generator):
    return next(generator)


def get_abtest_variations():
    return '%s%s' % (get_random_hash(), str(fake.unix_time()))


def get_temp_source_sku():
    return 'SOURCE-TMP-%s' % random.randint(10, 1000)


def get_random_spaces(length=random.randint(1, 30)):
    # '30' - limit the number of spaces
    return ' ' * length


def get_random_source_sku(simple=None):
    if not simple:
        simple = get_random_number_from_range(1, 4000)
    s1 = get_random_number_from_range(1, 10)
    s2 = get_random_number_from_range(1, 3)
    return "{}S{}S{}".format(simple, s1, s2)


def get_random_pet_status():
    return ",".join(random.sample(["creation", "edited", "images"], get_random_number_from_range(1, 3)))

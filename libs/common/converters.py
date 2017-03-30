from base64 import b64decode, b64encode
from hashlib import md5


def list_of_dict_to_string(list, dict_key):
    return ','.join([str(i[dict_key]) for i in list])


def get_ordered_json(json_obj):
    for k, v in json_obj.items():
        if isinstance(v, (list, tuple)):
            json_obj[k] = sorted(v)
        else:
            get_ordered_json(v)
    return json_obj


def remove_duplicates_from_lists(json_obj):
    for k, v in json_obj.items():
        if isinstance(v, (list, tuple)):
            json_obj[k] = list(set(v))
        else:
            remove_duplicates_from_lists(v)
    return json_obj


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def dict2obj(**my_dict):
    return Struct(**my_dict)


def remove_none_from_dict(json_obj):
    if isinstance(json_obj, dict):
        return {k: remove_none_from_dict(v) for k, v in json_obj.items() if k is not None and v is not None}
    elif isinstance(json_obj, list):
        return [remove_none_from_dict(item) for item in json_obj if item is not None]
    elif isinstance(json_obj, tuple):
        return tuple(remove_none_from_dict(item) for item in json_obj if item is not None)
    elif isinstance(json_obj, set):
        return {remove_none_from_dict(item) for item in json_obj if item is not None}
    else:
        return json_obj


def stringify(data, strictly=True):
    """ Convert data to <type: string> value """
    if type(data) == bytes:
        data = str(data, 'utf-8')
    return data


def unicodify(data, strictly=True):
    """ Convert data to <type: unicode> value """
    if strictly:
        if type(data) == str:
            return data.decode('utf-8')
    return data


def typify(data, cast=stringify, strictly=True):
    """ Typify all values recursively """

    iteratee = list(data) if type(data) == set else data
    if type(data) == tuple:
        new_data = []
        for i, item in enumerate(data):
            if hasattr(item, '__iter__'):
                item = typify(item, cast, strictly)
            new_data.append(cast(item, strictly))
        data = tuple(new_data)

    if type(data) in (list, set):
        for i, item in enumerate(iteratee):
            if hasattr(item, '__iter__'):
                item = typify(item, cast, strictly)
            if type(data) == set:
                data.remove(item)
                data.add(cast(item, strictly))
            else:
                data[i] = cast(item, strictly)

    if type(data) == dict:
        for i, name in enumerate(data):
            value = data[name]
            if hasattr(value, '__iter__'):
                data[name] = typify(value, cast, strictly)
            else:
                data[name] = cast(value, strictly)

    # TODO Add support for types from collections module (deque, OrderedDict and other)
    return data


def unify(data, data_type='string'):
    """ Cast string to appropriate type """

    if type(data) == bytes and data_type == 'string':
        data = str(data, 'utf-8')
    if type(data) == str and data_type == 'bytes':
        data = bytes(data, 'utf-8')
    return data


def encode_base64(string_data):
    """ Six-compatible base64 encoder """

    encoded_data = b64encode(string_data.encode('utf-8'))
    return str(encoded_data, 'utf-8')


def base64_decode(string_bytes):
    """ Six-compatible base64 decoder """

    decoded_bytes = b64decode(string_bytes.decode('utf-8'))
    return str(decoded_bytes, 'utf-8')


def md5_digest(data=''):
    """ """

    if type(data) == str:
        data = data.encode('utf-8')
    return md5(data).hexdigest()

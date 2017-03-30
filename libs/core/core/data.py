import datetime
import decimal
from json import JSONEncoder


class Encoder(JSONEncoder):
    def __init__(self, *args, **kwargs):
        super(Encoder, self).__init__(*args, **kwargs)

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%dT%H:%M:%S+00:00')
        return super(Encoder, self).default(o)


class SimpleEncoder(Encoder):
    def __init__(self, *args, **kwargs):
        super(SimpleEncoder, self).__init__(*args, **kwargs)


class FormattedEncoder(Encoder):
    def __init__(self, *args, **kwargs):
        kwargs['indent'] = 4
        kwargs['sort_keys'] = True
        super(FormattedEncoder, self).__init__(*args, **kwargs)

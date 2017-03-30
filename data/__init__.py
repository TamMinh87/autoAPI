error_schema = {
    'type': 'object',
    'properties': {
        'error': {
            'type': 'object',
            'properties': {
                'code': {'type': 'integer'},
                'message': {'type': 'string'},
                'data': {
                    'type': ['object', 'null']
                }
            },
            'required': ['code', 'message', 'data'],
            'additionalProperties': False
        }
    },
    'required': ['error'],
    'additionalProperties': False
}

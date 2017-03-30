import json

import jsonschema
import requests
from jsonschema import Draft3Validator

from libs.common.converters import get_ordered_json, unify
from libs.core.core.step import step


@step('Check code ok')
def check_code_ok(code, message='', **kwargs):
    assert requests.codes.ok == code, \
        "AssertionError. Response code was %s, expected %s, message was '%s'" % (
            code, requests.codes.ok, message)


@step('Check all codes are ok')
def check_codes_ok(responses, **kwargs):
    for response in responses:
        check_code_ok(response)


@step('Check code created')
def check_code_created(code, message='', **kwargs):
    assert requests.codes.created == code, message


@step('Check 500 code internal server error')
def check_code_server_error(code, message='', **kwargs):
    assert requests.codes.server_error == code, message


@step('Validate json schema')
def validate_json_schema(response, schema, **kwargs):
    jsonschema.validate(response, schema)


@step('Soft validate json schema')
def soft_validate_jsonschema(response, schema):
    errors = []
    validator = Draft3Validator(schema)
    for error in validator.iter_errors(response):
        errors.append(error)
    return errors


@step('Check code moved permanently')
def check_code_moved(code, message='', **kwargs):
    assert requests.codes.moved == code, message


@step('Check code moved temporary')
def check_code_found(code, message='', **kwargs):
    assert requests.codes.found == code, message


@step('Validate full json data')
def validate_full_json(json_obj_master, json_obj_slave, **kwargs):
    if get_ordered_json(json_obj_master) != get_ordered_json(json_obj_slave):
        raise AssertionError('Json\'s are not equal')


@step('Check 400 code bad request')
def check_code_bad_request(code, message='', **kwargs):
    assert requests.codes.bad_request == code, message


@step('Check 404 code not found')
def check_code_not_found(code, message='', **kwargs):
    assert requests.codes.not_found == code, message


@step("Check error message")
def check_error_message(response, error_message, partial=False, **kwargs):
    if partial:
        assert (error_message in response.get('error_message'))
    else:
        assert (response.get('error_message') == error_message)


@step("Check if it is json")
def is_json(val, **kwargs):
    try:
        json.loads(unify(val))
    except ValueError:
        return False
    return True

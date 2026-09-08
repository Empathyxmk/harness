import pytest
from pynubank import MockHttpClient
from pynubank.exception import NuException
from pynubank.nubank import Nubank
from datetime import datetime
from uuid import uuid4
import inspect

@pytest.fixture(scope="module")
def nubank_client_public():
    client = Nubank(client=MockHttpClient())
    # Use a different CPF/password/uuid than in the original test
    client.authenticate_with_qr_code('22233344455', 'public_pw', 'uuid-public')
    return client

def test_get_invalid_url_should_throw_exception_public():
    client = MockHttpClient()
    with pytest.raises(NuException):
        client.get('another.invalid.url')

def test_post_invalid_url_should_throw_exception_public():
    client = MockHttpClient()
    with pytest.raises(NuException):
        client.post('another.invalid.url', {})

def test_check_not_tested_new_methods_public(nubank_client_public):
    # Copy the logic but use different keys/values
    default_params = {
        'get_bill_details': {
            'bill': {'_links': {'self': {'href': 'https://mocked-proxy-url/api/bills/12345-test-bill'}}}
        },
        'get_account_investments_yield': {
            'date': datetime.min,
        },
        'get_card_statement_details': {
            'statement': {'_links': {'self': {'href': f'https://mocked-proxy-url/api/transactions/{uuid4()}'}}},
        },
        'authenticate_with_cert': {
            'cpf': '22233344455',
            'password': 'public_pw',
            'cert_data': b'public_cert_data',
        },
        'authenticate_with_refresh_token': {
            'refresh_token': 'public_refresh_token',
            'cert_data': b'public_cert_data',
        }
    }

    methods = dir(nubank_client_public)
    for method_name in methods:
        method = getattr(nubank_client_public, method_name)
        if method_name[0] != '_' and callable(method):
            args = list(range(get_method_arg_count_public(method) - 1))
            params = default_params.get(method_name)
            if params is None:
                params = inspect.signature(method).parameters
            for index, name in enumerate(params):
                args[index] = params[name].annotation() if type(params[name]) == inspect.Parameter else params[name]
            try:
                method(*args)
            except Exception as ex:
                print(f'{method_name} is missing a mock !!')
                raise ex

def get_method_arg_count_public(method):
    try:
        return method.__wrapped__.__code__.co_argcount
    except AttributeError:
        return method.__code__.co_argcount
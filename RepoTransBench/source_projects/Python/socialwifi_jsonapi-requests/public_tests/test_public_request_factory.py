from unittest import mock

import pytest
import requests

from jsonapi_requests import configuration
from jsonapi_requests import data
from jsonapi_requests import request_factory


@pytest.fixture
def api_configuration():
    # Change API_ROOT and RETRIES to different values
    return configuration.Factory({'API_ROOT': 'mockapi', 'RETRIES': 3}).create()


@pytest.fixture
def request_mock():
    with mock.patch('requests.request') as mocked:
        yield mocked


@pytest.fixture
def valid_response():
    response = mock.Mock(status_code=201)  # Different valid status
    response.json.return_value = {'message': 'created'}
    return response


def test_get_public(api_configuration, request_mock, valid_response):
    request_mock.return_value = valid_response
    response = request_factory.ApiRequestFactory(api_configuration).get('different_endpoint')
    assert response.content == data.JsonApiResponse.from_data({'message': 'created'})


def test_retrying_public(api_configuration, request_mock, valid_response):
    request_mock.side_effect = [requests.Timeout, requests.Timeout, valid_response]
    response = request_factory.ApiRequestFactory(api_configuration).get('another_endpoint')
    assert response.content == data.JsonApiResponse.from_data({'message': 'created'})


def test_reraises_public(api_configuration, request_mock, valid_response):
    # Will exceed retries (set to 3) all fail
    request_mock.side_effect = [requests.Timeout, requests.Timeout, requests.Timeout, valid_response]
    with pytest.raises(request_factory.ApiConnectionError):
        request_factory.ApiRequestFactory(api_configuration).get('fail_endpoint')
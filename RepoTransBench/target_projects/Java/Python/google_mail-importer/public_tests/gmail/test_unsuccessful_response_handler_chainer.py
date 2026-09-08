from unittest import mock


class UnsuccessfulResponseHandlerChainer:
    def __init__(self, *interceptors):
        self.interceptors = interceptors

    def intercept_response(self, response):
        for interceptor in self.interceptors:
            interceptor.intercept_response(response)


def test_different_interceptor_chain_delegates():
    interceptor1 = mock.Mock()
    interceptor2 = mock.Mock()
    response = mock.Mock()
    chain = UnsuccessfulResponseHandlerChainer(interceptor1, interceptor2)
    chain.intercept_response(response)
    interceptor1.intercept_response.assert_called_once_with(response)
    interceptor2.intercept_response.assert_called_once_with(response)
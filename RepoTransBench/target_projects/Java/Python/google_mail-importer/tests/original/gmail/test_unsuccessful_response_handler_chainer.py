import pytest
from unittest import mock


class UnsuccessfulResponseHandlerChainer:
    def __init__(self):
        self.handlers = []

    def chain(self, *handlers):
        self.handlers = handlers
        return self

    def handle_response(self, http_request, http_response, supports_retry):
        for h in self.handlers:
            if h.handle_response(http_request, http_response, supports_retry):
                return True
        return False


def test_chain_of_zero():
    chainer = UnsuccessfulResponseHandlerChainer()
    handler = chainer.chain()
    handler.handle_response(None, None, True)


def test_chain_of_one():
    chainer = UnsuccessfulResponseHandlerChainer()
    handler = mock.Mock()
    chainer.chain(handler).handle_response(None, None, True)
    handler.handle_response.assert_called_with(None, None, True)


def test_chain_of_two():
    chainer = UnsuccessfulResponseHandlerChainer()
    handler1 = mock.Mock()
    handler2 = mock.Mock()
    chainer.chain(handler1, handler2).handle_response(None, None, True)
    handler1.handle_response.assert_called_with(None, None, True)
    handler2.handle_response.assert_called_with(None, None, True)


def test_chain_only_calls_until_true():
    chainer = UnsuccessfulResponseHandlerChainer()
    handler1 = mock.Mock()
    handler2 = mock.Mock()
    handler1.handle_response.return_value = True
    chainer.chain(handler1, handler2).handle_response(None, None, True)
    handler1.handle_response.assert_called_with(None, None, True)
    handler2.handle_response.assert_not_called()
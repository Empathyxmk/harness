import base64
from threading import Event

from pytest import raises

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pywebostv.controls
from pywebostv.controls import WebOSControlBase
from pywebostv.controls import arguments, process_payload
from pywebostv.model import Application

from tests.utils import FakeClient

class TestArgumentExtractionPublic(object):
    def test_bad_argument_param_public(self):
        with raises(ValueError):
            arguments([])  # Use a list instead of None or dict

        with raises(ValueError):
            arguments("")

    def test_extract_positional_args_public(self):
        args = arguments(0)
        assert args("x", "y", "z") == "x"

        with raises(TypeError):
            assert args()

    def test_extract_keyword_args_public(self):
        args = arguments("foo")
        assert args(foo=123) == 123

        with raises(TypeError):
            assert args(bar=1)

    def test_args_default_value_public(self):
        args = arguments(1, default={3, 4})
        assert args() == {3, 4}
        assert args("onlyme") == "onlyme"

    def test_kwargs_default_value_public(self):
        args = arguments("a", default="defaultvalue")
        assert args() == "defaultvalue"
        assert args(a="something else") == "something else"

    def test_postprocess_public(self):
        args = arguments(0, postprocess=lambda x: 9001, default=13)
        assert args() == 13
        assert args("ignored") == 9001

class TestProcessPayloadPublic(object):
    def test_process_payload_public(self):
        payload = {
            "layer1": {
                "layer2": [9, 8],
                "layer2a": lambda *a, **b: "{}|{}".format(sum(a), len(b))
            },
            "layer1a": {7, 8}
        }
        expected = {
            "layer1": {
                "layer2": [9, 8],
                "layer2a": "17|0"
            },
            "layer1a": {7, 8}
        }
        assert process_payload(payload, 9, 8) == expected

    def test_just_callable_arg_public(self):
        assert process_payload(lambda x: x + 10, 15) == 25

class TestWebOSControlBasePublic(object):
    def test_missing_attribute_public(self):
        client = FakeClient()
        control_base = WebOSControlBase(client)
        control_base.COMMANDS = {}
        with raises(AttributeError):
            control_base.not_present_attr()

    def test_exec_command_blocking_public(self):
        client = FakeClient()
        control_base = WebOSControlBase(client)
        control_base.COMMANDS = {
            "foo": {"uri": "/foo"}
        }

        client.setup_response("/foo", {"bar": "yes"})
        assert control_base.foo() == {"bar": "yes"}

    def test_exec_command_callback_public(self):
        client = FakeClient()
        control_base = WebOSControlBase(client)
        control_base.COMMANDS = {
            "foo": {"uri": "/foo"}
        }

        response = []
        event = Event()

        def callback(status, resp):
            response.append((status, resp))
            event.set()

        client.setup_response("/foo", {"bar": "baz"})
        control_base.foo(callback=callback)
        event.wait()

        assert response == [(True, {"bar": "baz"})]

    def test_exec_command_failed_callback_public(self):
        client = FakeClient()
        control_base = WebOSControlBase(client)
        control_base.COMMANDS = {
            "fail": {
                "uri": "/fail",
                "validation": lambda *args: (False, "public-error"),
                "validation_error": "ErrMsg"
            }
        }

        response = []
        event = Event()

        def callback(status, resp):
            response.append((status, resp))
            event.set()

        client.setup_response("/fail", {"foo": "bar"})
        control_base.fail(callback=callback)
        event.wait()

        assert response == [(False, "public-error")]

    def test_exec_command_failed_blocking_public(self):
        client = FakeClient()
        control_base = WebOSControlBase(client)
        control_base.COMMANDS = {
            "fail": {
                "uri": "/fail",
                "validation": lambda *args: (False, "broken"),
                "validation_error": "broken"
            },
        }

        client.setup_response("/fail", {"foo": "bar"})
        with raises(IOError):
            control_base.fail(block=True)

    def test_exec_timeout_public(self):
        client = FakeClient()
        control_base = WebOSControlBase(client)
        control_base.COMMANDS = {
            "foo": {
                "uri": "/foo",
            },
        }

        client.setup_response("/not-foo", {"xyz": True})
        with raises(Exception):
            control_base.foo(timeout=1)

    def test_subscribe_public(self):
        client = FakeClient()
        control_base = WebOSControlBase(client)
        control_base.COMMANDS = {
            "foo": {
                "uri": "/foo",
                "subscription": True,
                "subscription_validation": lambda p: (p == {"c": 10}, "Oops.")
            },
        }

        resp = []
        e1, e2 = Event(), Event()
        events = [e1, e2]

        def callback(status, payload):
            resp.append((status, payload))
            events.pop(0).set()

        client.setup_subscribe_response("/foo", [{"c": 10}, {"c": 20}])
        control_base.subscribe_foo(callback)
        assert e1.wait(timeout=2)
        assert e2.wait(timeout=2)

        assert resp == [(True, {"c": 10}), (False, "Oops.")]

        with raises(ValueError):
            control_base.subscribe_foo(None)

    def test_subscription_not_found_public(self):
        client = FakeClient()
        control_base = WebOSControlBase(client)
        control_base.COMMANDS = {
            "foo": {
                "uri": "/foo",
                "subscription": True
            },
        }

        with raises(AttributeError):
            control_base.subscribe_bar(None)

        with raises(AttributeError):
            control_base.unsubscribe_bar()

    def test_subscription_not_allowed_public(self):
        client = FakeClient()
        control_base = WebOSControlBase(client)
        control_base.COMMANDS = {
            "foo": {
                "uri": "/foo",
            },
        }
        with raises(AttributeError):
            control_base.subscribe_foo(None)

        with raises(AttributeError):
            control_base.unsubscribe_foo()
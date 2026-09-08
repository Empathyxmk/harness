import json
import time
from queue import Empty
from threading import Event, Thread

from pytest import raises

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pywebostv.connection
from pywebostv.connection import WebOSClient

from tests.utils import FakeClient


class TestWebOSClientPublic(object):
    def test_unique_id_public(self):
        uid = "#87"
        client = FakeClient()
        client.send_message('rsp', 'urn', {"val": "data"}, unique_id=uid)

        client.assert_sent_message({
            "id": "#87",
            "payload": {"val": "data"},
            "type": "rsp",
            "uri": "urn"
        })

    def test_get_queue_public(self):
        client = FakeClient()
        queue = client.send_message('ntf', 'test/uri', {"foo": "bar"},
                                    unique_id="42", get_queue=True)
        client.received_message(json.dumps({"id": "42", "data": "foobar"}))

        assert queue.get(block=True, timeout=1) == dict(id="42", data="foobar")

    def test_send_callback_public(self):
        obj = {}

        def callback(res):
            obj["called"] = res

        client = FakeClient()
        client.send_message('req', 'abc', {"hello": "world"},
                            callback=callback, unique_id="99")
        client.received_message(json.dumps({"id": "99", "res": 123}))

        assert obj["called"] == dict(id="99", res=123)

    def test_send_minimum_params_public(self):
        client = FakeClient()
        client.send_message('rsp', "foobar", None, unique_id="11")

        client.assert_sent_message({"uri": "foobar", "type": "rsp", "id": "11"})

    def test_multiple_send_public(self):
        client = FakeClient()
        q1 = client.send_message('ntf', "hello/world", None, unique_id="7",
                                 get_queue=True)
        q2 = client.send_message('req', "hello/world", None, unique_id="9",
                                 get_queue=True)

        client.received_message(json.dumps({"id": "9", "cool": "beans"}))
        client.received_message(json.dumps({"id": "7", "foo": "bar"}))

        assert q1.get(block=True, timeout=1) == {"id": "7", "foo": "bar"}
        assert q2.get(block=True, timeout=1) == {"id": "9", "cool": "beans"}

    def test_clear_waiters_public(self):
        client = FakeClient()
        q1 = client.send_message('rsp', "abc/", None, unique_id="30",
                                 get_queue=True,
                                 cur_time=lambda: time.time() - 99)
        q2 = client.send_message('ntf', "xyz/", None, unique_id="40",
                                 get_queue=True,
                                 cur_time=lambda: time.time() - 10)

        client.received_message(json.dumps({"id": "40", "abc": "xyz"}))
        client.received_message(json.dumps({"id": "30", "bar": "baz"}))

        with raises(Empty):
            assert q1.get(block=True, timeout=1)

        assert q2.get(block=True, timeout=1) == {"id": "40", "abc": "xyz"}

    def test_subscription_public(self):
        result = []
        result_event = Event()

        def callback(obj):
            result.append(obj)
            result_event.set()

        client = FakeClient()
        client.subscribe('alt_uri', "321", callback)

        client.received_message(json.dumps({"id": "321", "payload": [10]}))
        client.received_message(json.dumps({"id": "321", "payload": [20]}))
        client.received_message(json.dumps({"id": "321", "payload": [30]}))

        result_event.wait()
        assert result == [[10], [20], [30]]

        result = []
        client.unsubscribe("321")

        client.received_message(json.dumps({"id": "321", "payload": [100]}))
        assert result == []

        with raises(ValueError):
            client.unsubscribe("321")

    def test_new_registration_public(self):
        client = FakeClient()
        store = {}
        with raises(Exception):
            next(client.register(store, timeout=1))

        assert 'client-key' not in json.dumps(client.sent_message)

        store["client_key"] = "NEW-KEY-456!"

        with raises(Exception):
            next(client.register(store, timeout=1))

        assert 'NEW-KEY-456!' in json.dumps(client.sent_message)

    def test_discovery_public(self):
        def mock_discover(*args, **kwargs):
            return ["hostA", "hostB"]
        backup = pywebostv.connection.discover
        pywebostv.connection.discover = mock_discover

        expected = ["ws://{}:3000/".format(x) for x in ["hostA", "hostB"]]
        assert [x.url for x in WebOSClient.discover()] == expected

        pywebostv.connection.discover = backup

    def test_registration_timeout_public(self):
        client = FakeClient()
        with raises(Exception):
            list(client.register({}, timeout=3))

    def test_registration_public(self):
        client = FakeClient()
        sent_event = Event()

        def make_response(prompt, registered, wrong):
            def send_response():
                sent_event.wait()
                sent_event.clear()

                if prompt:
                    client.received_message(json.dumps({
                        "id": "2",
                        "payload": {"pairingType": "PROMPT"}
                    }))
                if registered:
                    client.received_message(json.dumps({
                        "id": "2",
                        "payload": {"client-key": "publicxyz"},
                        "type": "registered"
                    }))
                if wrong:
                    client.received_message(json.dumps({
                        "id": "2",
                        "type": "wrong-response"
                    }))
            return send_response

        def patched_send_message(*args, **kwargs):
            kwargs["unique_id"] = "2"
            obj = WebOSClient.send_message(client, *args, **kwargs)
            sent_event.set()
            return obj

        client.send_message = patched_send_message

        store = {}
        Thread(target=make_response(True, True, False)).start()
        gen = client.register(store, timeout=10)
        assert next(gen) == WebOSClient.PROMPTED
        assert next(gen) == WebOSClient.REGISTERED

        assert store == {"client_key": "publicxyz"}

        # Test with non-empty store.
        Thread(target=make_response(False, True, False)).start()
        assert list(client.register(store, timeout=10)) ==\
            [WebOSClient.REGISTERED]
        assert "publicxyz" in json.dumps(client.sent_message)

        # Test wrong response.
        Thread(target=make_response(False, False, True)).start()
        with raises(Exception):
            list(client.register(store, timeout=10))
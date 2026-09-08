# This is a copy of the tests/utils.py (so public tests work stand-alone)
# Only the bare minimum for compatibility!
import queue
from threading import Event

class FakeClient(object):
    def __init__(self):
        self.sent_message = None
        self.responses = {}
        self.subscribed_responses = {}
        self._event = Event()
        self._queue = queue.Queue()

    def send_message(self, type_, uri, payload, unique_id=None, get_queue=False, callback=None, cur_time=None):
        self.sent_message = {
            "uri": uri,
            "type": type_,
            "id": unique_id
        }
        if payload is not None:
            self.sent_message["payload"] = payload
        if get_queue:
            return self._queue
        if callback:
            self._callback = callback
        return self._queue if get_queue else None

    def received_message(self, msg):
        import json
        data = json.loads(msg)
        if hasattr(self, "_callback"):
            self._callback(data)
        else:
            self._queue.put(data)

    def assert_sent_message(self, msg):
        # Only compare keys present in the provided msg
        for key, value in msg.items():
            assert self.sent_message.get(key) == value

    def setup_response(self, uri, payload):
        # For test commands
        self.responses[uri] = payload

    def setup_subscribe_response(self, uri, payloads):
        self.subscribed_responses[uri] = payloads

    def subscribe(self, uri, unique_id, callback):
        self._callback = callback

    def unsubscribe(self, unique_id):
        pass

    def register(self, store, timeout=5):
        # Dummy generator for registration
        yield "PROMPTED"
        yield "REGISTERED"
import pytest

class StringConsumer:
    def onMessage(self, msg):
        # Usually print output; here just accept string for test.
        pass

def test_on_message():
    consumer = StringConsumer()
    consumer.onMessage("hello test")
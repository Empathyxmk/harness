from pocketsphinx.recognition_listener import RecognitionListener
from pocketsphinx.hypothesis import Hypothesis

class CallbackCounter(RecognitionListener):
    def __init__(self):
        self.ready = 0
        self.begin = 0
        self.end = 0
        self.partial = 0
        self.result = 0
        self.error = 0
        self.timeout = 0

    def onReadyForSpeech(self):
        self.ready += 1

    def onBeginningOfSpeech(self):
        self.begin += 1

    def onEndOfSpeech(self):
        self.end += 1

    def onPartialResult(self, hypothesis):
        self.partial += 1

    def onResult(self, hypothesis):
        self.result += 1

    def onError(self, e):
        self.error += 1

    def onTimeout(self):
        self.timeout += 1

def test_listener_methods():
    cc = CallbackCounter()
    cc.onReadyForSpeech()
    cc.onBeginningOfSpeech()
    cc.onEndOfSpeech()
    cc.onPartialResult(Hypothesis("foo", 10))
    cc.onResult(Hypothesis("bar", 9))
    cc.onError(Exception("fail"))
    cc.onTimeout()
    assert cc.ready == 1
    assert cc.begin == 1
    assert cc.end == 1
    assert cc.partial == 1
    assert cc.result == 1
    assert cc.error == 1
    assert cc.timeout == 1
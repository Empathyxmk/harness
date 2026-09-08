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

def test_listener_methods_with_different_data():
    cc = CallbackCounter()
    cc.onReadyForSpeech()
    cc.onReadyForSpeech()  # Call twice to differ from existing
    cc.onBeginningOfSpeech()
    cc.onPartialResult(Hypothesis("different_partial", 100))
    cc.onEndOfSpeech()
    cc.onEndOfSpeech()  # Call twice to differ from existing
    cc.onResult(Hypothesis("different_result", 99))
    cc.onResult(Hypothesis("result_again", -5))
    cc.onError(Exception("different_fail"))
    cc.onError(Exception("another_fail"))
    cc.onTimeout()
    cc.onTimeout()  # Call twice to differ

    assert cc.ready == 2
    assert cc.begin == 1
    assert cc.end == 2
    assert cc.partial == 1
    assert cc.result == 2
    assert cc.error == 2
    assert cc.timeout == 2
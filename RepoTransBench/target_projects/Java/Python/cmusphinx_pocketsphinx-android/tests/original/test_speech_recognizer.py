from pocketsphinx.speech_recognizer import SpeechRecognizer
from pocketsphinx.recognition_listener import RecognitionListener
from pocketsphinx.hypothesis import Hypothesis

class DummyListener(RecognitionListener):
    def __init__(self):
        self.ready = False

    def onReadyForSpeech(self):
        self.ready = True

    def onBeginningOfSpeech(self):
        pass

    def onEndOfSpeech(self):
        pass

    def onPartialResult(self, hypothesis):
        pass

    def onResult(self, hypothesis):
        pass

    def onError(self, e):
        pass

    def onTimeout(self):
        pass

def test_add_and_remove_listener():
    recognizer = SpeechRecognizer()
    l = DummyListener()
    recognizer.addListener(l)
    recognizer.removeListener(l)
    # Should not cause exceptions

def test_start_listening_fires_ready():
    recognizer = SpeechRecognizer()
    l = DummyListener()
    recognizer.addListener(l)
    recognizer.startListening("search")
    assert l.ready

def test_stop_and_cancel_no_errors():
    recognizer = SpeechRecognizer()
    recognizer.stop()
    recognizer.cancel()
    # Just for coverage, no state to assert
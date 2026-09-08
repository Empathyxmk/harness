from pocketsphinx.speech_recognizer_setup import SpeechRecognizerSetup
import os

def test_default_setup():
    setup = SpeechRecognizerSetup.defaultSetup()
    assert setup is not None

def test_get_recognizer_returns_speech_recognizer():
    setup = SpeechRecognizerSetup.defaultSetup()
    setup.setAcousticModel(".")
    setup.setDictionary(".")
    setup.setRawLogDir(".")
    recognizer = setup.getRecognizer()
    assert recognizer is not None

def test_set_key_methods():
    setup = SpeechRecognizerSetup.defaultSetup()
    assert setup.setAcousticModel(".") is setup
    assert setup.setDictionary(".") is setup
    assert setup.setRawLogDir(".") is setup
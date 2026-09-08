from pocketsphinx.speech_recognizer import SpeechRecognizer

def test_speech_recognizer_instance_public():
    recognizer = SpeechRecognizer()
    assert recognizer is not None

# Note: Cannot test much more in public environment without Android context
from pocketsphinx.speech_recognizer_setup import SpeechRecognizerSetup

def test_default_setup_returns_setup_instance_public():
    setup = SpeechRecognizerSetup.defaultSetup()
    assert setup is not None

def test_setup_with_non_existing_files_public():
    setup = SpeechRecognizerSetup.defaultSetup()
    acoustic_model = "dummy_model_dir_public"
    dictionary = "dummy_dict_file_public.dic"
    log_dir = "dummy_log_dir_public"
    assert setup.setAcousticModel(acoustic_model) is setup
    assert setup.setDictionary(dictionary) is setup
    assert setup.setRawLogDir(log_dir) is setup

def test_get_recognizer_returns_instance_public():
    setup = SpeechRecognizerSetup.defaultSetup()
    assert setup.getRecognizer() is not None
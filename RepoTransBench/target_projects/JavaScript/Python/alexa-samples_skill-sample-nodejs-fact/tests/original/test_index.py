from src.alexafact.index import supportsInterface, supportsAPL

def test_supportsInterface_true_when_present():
    handlerInput = {
        'requestEnvelope': {
            'context': {
                'System': {
                    'device': {
                        'supportedInterfaces': {
                            'Alexa.Presentation.APL': {}
                        }
                    }
                }
            }
        }
    }
    assert supportsInterface(handlerInput, 'Alexa.Presentation.APL') is True

def test_supportsInterface_false_when_undefined():
    handlerInput = {
        'requestEnvelope': {
            'context': {
                'System': {
                    'device': {
                        'supportedInterfaces': {}
                    }
                }
            }
        }
    }
    assert supportsInterface(handlerInput, 'Alexa.Presentation.APL') is False

def test_supportsInterface_handles_missing_properties():
    examples = [
        {},
        {'requestEnvelope': {}},
        {'requestEnvelope': {'context': {}}},
        {'requestEnvelope': {'context': {'System': {}}}},
        {'requestEnvelope': {'context': {'System': {'device': {}}}}}
    ]
    for obj in examples:
        assert supportsInterface(obj, 'Alexa.Presentation.APL') is False

def test_supportsInterface_false_if_entry_null():
    handlerInput = {
        'requestEnvelope': {
            'context': {
                'System': {
                    'device': {
                        'supportedInterfaces': {'Alexa.Presentation.APL': None}
                    }
                }
            }
        }
    }
    assert supportsInterface(handlerInput, 'Alexa.Presentation.APL') is False

def test_supportsAPL_true_when_supported():
    handlerInput = {
        'requestEnvelope': {
            'context': {
                'System': {
                    'device': {
                        'supportedInterfaces': {'Alexa.Presentation.APL': {'something': True}}
                    }
                }
            }
        }
    }
    assert supportsAPL(handlerInput) is True

def test_supportsAPL_false_when_not_supported():
    handlerInput = {
        'requestEnvelope': {
            'context': {
                'System': {
                    'device': {
                        'supportedInterfaces': {}
                    }
                }
            }
        }
    }
    assert supportsAPL(handlerInput) is False
from src.alexafact.index import supportsInterface

def test_supportsInterface_public_true_if_supported():
    handlerInput = {
        'requestEnvelope': {
            'context': {
                'System': {
                    'device': {
                        'supportedInterfaces': {
                            'AudioPlayer': {}
                        }
                    }
                }
            }
        }
    }
    assert supportsInterface(handlerInput, 'AudioPlayer') is True
    assert supportsInterface(handlerInput, 'Display') is False

def test_supportsInterface_public_falsy_inputs():
    assert supportsInterface({}, 'AudioPlayer') is False
    assert supportsInterface('', 'Display') is False
    assert supportsInterface(0, 'VideoApp') is False
    assert supportsInterface(False, 'VideoApp') is False

def test_supportsInterface_public_missing_properties():
    assert supportsInterface({'requestEnvelope': {}}, 'AudioPlayer') is False
    assert supportsInterface({'requestEnvelope': {'context': None}}, 'AudioPlayer') is False
    assert supportsInterface({'requestEnvelope': {'context': {'System': {}}}}, 'AudioPlayer') is False
    assert supportsInterface({'requestEnvelope': {'context': {'System': {'device': {}}}}}, 'AudioPlayer') is False

def test_supportsInterface_public_custom_interface():
    handlerInput = {
        'requestEnvelope': {
            'context': {
                'System': {
                    'device': {
                        'supportedInterfaces': {
                            'CustomInterface': {},
                            'VideoApp': {}
                        }
                    }
                }
            }
        }
    }
    assert supportsInterface(handlerInput, 'CustomInterface') is True
    assert supportsInterface(handlerInput, 'VideoApp') is True
    assert supportsInterface(handlerInput, 'GameEngine') is False

def test_supportsInterface_public_odd_property_names():
    handlerInput = {
        'requestEnvelope': {
            'context': {
                'System': {
                    'device': {
                        'supportedInterfaces': {
                            'myWeird-Interface_B56': {}
                        }
                    }
                }
            }
        }
    }
    assert supportsInterface(handlerInput, 'myWeird-Interface_B56') is True
    assert supportsInterface(handlerInput, 'AnotherOne') is False
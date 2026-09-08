import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import sys

sys.modules['src.alexafact.personalizationUtil'] = __import__('src.alexafact.personalizationUtil', fromlist=['*'])

from src.alexafact import personalizationStorageUtil

@patch('src.alexafact.personalizationUtil.getPerson')
def test_savePreference_public_saves_if_getPerson_true(mock_getPerson):
    mock_getPerson.return_value = True
    setPersistentAttributes = MagicMock()
    savePersistentAttributes = MagicMock()
    handlerInput = {'attributesManager': {
        'setPersistentAttributes': setPersistentAttributes,
        'savePersistentAttributes': savePersistentAttributes
    }}
    personalizationStorageUtil.savePreference(handlerInput, {"baz": "qux"})
    setPersistentAttributes.assert_called_once_with({'baz': 'qux'})
    savePersistentAttributes.assert_called_once()

@patch('src.alexafact.personalizationUtil.getPerson')
def test_savePreference_public_not_save_if_getPerson_falsy(mock_getPerson):
    mock_getPerson.return_value = None
    handlerInput = {'attributesManager': {
        'setPersistentAttributes': MagicMock(),
        'savePersistentAttributes': MagicMock()
    }}
    personalizationStorageUtil.savePreference(handlerInput, {"baz": "qux"})
    handlerInput['attributesManager']['setPersistentAttributes'].assert_not_called()
    handlerInput['attributesManager']['savePersistentAttributes'].assert_not_called()

def test_setAttribute_public_sets_key_value():
    result = personalizationStorageUtil.setAttribute('alpha', 'beta')
    assert result == {'key': 'alpha', 'value': 'beta'}

def test_addAttribute_public_adds_to_message():
    message = {'another': 10}
    personalizationStorageUtil.addAttribute(message, 'plusKey', 20)
    assert message == {'another': 10, 'key': 'plusKey', 'value': 20}

@patch('src.alexafact.personalizationUtil.getPerson')
@pytest.mark.asyncio
async def test_getPreference_public_gets_if_getPerson_true(mock_getPerson):
    mock_getPerson.return_value = True
    getPersistentAttributes = AsyncMock(return_value={'custom': 42})
    handlerInput = {'attributesManager': {'getPersistentAttributes': getPersistentAttributes}}
    result = await personalizationStorageUtil.getPreference(handlerInput)
    assert result == {'custom': 42}

@patch('src.alexafact.personalizationUtil.getPerson')
@pytest.mark.asyncio
async def test_getPreference_public_not_get_if_getPerson_falsy(mock_getPerson):
    mock_getPerson.return_value = None
    handlerInput = {'attributesManager': {'getPersistentAttributes': AsyncMock()}}
    result = await personalizationStorageUtil.getPreference(handlerInput)
    assert result is None

@patch('src.alexafact.personalizationUtil.getPerson')
@pytest.mark.asyncio
async def test_getPreferenceOrDefault_public_gets_if_getPerson_true(mock_getPerson):
    mock_getPerson.return_value = True
    getPersistentAttributes = AsyncMock(return_value={'pref': 99})
    handlerInput = {'attributesManager': {'getPersistentAttributes': getPersistentAttributes}}
    result = await personalizationStorageUtil.getPreferenceOrDefault(handlerInput, {'default': 'y'})
    assert result == {'pref': 99}

@patch('src.alexafact.personalizationUtil.getPerson')
@pytest.mark.asyncio
async def test_getPreferenceOrDefault_public_returns_default_if_getPerson_false(mock_getPerson):
    mock_getPerson.return_value = False
    handlerInput = {'attributesManager': {'getPersistentAttributes': AsyncMock()}}
    defaultObj = {'foo': 'bar'}
    result = await personalizationStorageUtil.getPreferenceOrDefault(handlerInput, defaultObj)
    assert result == defaultObj

def test_setAttribute_public_handles_undefined_value():
    result = personalizationStorageUtil.setAttribute('foozle')
    assert result == {'key': 'foozle', 'value': None}

def test_addAttribute_public_handles_undefined_value():
    obj = {}
    personalizationStorageUtil.addAttribute(obj, 'yolo')
    assert obj == {'key': 'yolo', 'value': None}
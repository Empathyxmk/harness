import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import sys

sys.modules['src.alexafact.personalizationUtil'] = __import__('src.alexafact.personalizationUtil', fromlist=['*'])

from src.alexafact import personalizationStorageUtil

@pytest.fixture(autouse=True)
def clear_imports(monkeypatch):
    # Clear mocked getPerson for each test
    if hasattr(personalizationStorageUtil, 'personalizationUtil'):
        personalizationStorageUtil.personalizationUtil.getPerson = lambda _: None
    yield

@patch('src.alexafact.personalizationUtil.getPerson')
def test_savePreference_saves_if_getPerson_true(mock_getPerson):
    mock_getPerson.return_value = True
    setPersistentAttributes = MagicMock()
    savePersistentAttributes = MagicMock()
    handlerInput = {'attributesManager': {
        'setPersistentAttributes': setPersistentAttributes,
        'savePersistentAttributes': savePersistentAttributes
    }}
    personalizationStorageUtil.savePreference(handlerInput, {"foo": "bar"})
    setPersistentAttributes.assert_called_once_with({'foo': 'bar'})
    savePersistentAttributes.assert_called_once()

@patch('src.alexafact.personalizationUtil.getPerson')
def test_savePreference_not_save_if_getPerson_falsy(mock_getPerson):
    mock_getPerson.return_value = False
    handlerInput = {'attributesManager': {
        'setPersistentAttributes': MagicMock(),
        'savePersistentAttributes': MagicMock()
    }}
    personalizationStorageUtil.savePreference(handlerInput, {"foo": "bar"})
    handlerInput['attributesManager']['setPersistentAttributes'].assert_not_called()
    handlerInput['attributesManager']['savePersistentAttributes'].assert_not_called()

def test_setAttribute_sets_key_value():
    result = personalizationStorageUtil.setAttribute('testKey', 'testValue')
    assert result == {'key': 'testKey', 'value': 'testValue'}

def test_addAttribute_adds_to_message():
    message = {'prop': 1}
    personalizationStorageUtil.addAttribute(message, 'newKey', 2)
    assert message == {'prop': 1, 'key': 'newKey', 'value': 2}

@patch('src.alexafact.personalizationUtil.getPerson')
@pytest.mark.asyncio
async def test_getPreference_gets_if_getPerson_true(mock_getPerson):
    mock_getPerson.return_value = True
    getPersistentAttributes = AsyncMock(return_value={'pref': 1})
    handlerInput = {'attributesManager': {'getPersistentAttributes': getPersistentAttributes}}
    result = await personalizationStorageUtil.getPreference(handlerInput)
    assert result == {'pref': 1}

@patch('src.alexafact.personalizationUtil.getPerson')
@pytest.mark.asyncio
async def test_getPreference_not_get_if_getPerson_falsy(mock_getPerson):
    mock_getPerson.return_value = False
    handlerInput = {'attributesManager': {'getPersistentAttributes': AsyncMock()}}
    result = await personalizationStorageUtil.getPreference(handlerInput)
    assert result is None

@patch('src.alexafact.personalizationUtil.getPerson')
@pytest.mark.asyncio
async def test_getPreferenceOrDefault_gets_if_getPerson_true(mock_getPerson):
    mock_getPerson.return_value = True
    getPersistentAttributes = AsyncMock(return_value={'pref': 2})
    handlerInput = {'attributesManager': {'getPersistentAttributes': getPersistentAttributes}}
    result = await personalizationStorageUtil.getPreferenceOrDefault(handlerInput, {'default': 'x'})
    assert result == {'pref': 2}

@patch('src.alexafact.personalizationUtil.getPerson')
@pytest.mark.asyncio
async def test_getPreferenceOrDefault_returns_default_if_getPerson_false(mock_getPerson):
    mock_getPerson.return_value = False
    handlerInput = {'attributesManager': {'getPersistentAttributes': AsyncMock()}}
    defaultObj = {'default': True}
    result = await personalizationStorageUtil.getPreferenceOrDefault(handlerInput, defaultObj)
    assert result == defaultObj

def test_setAttribute_handles_undefined_value():
    result = personalizationStorageUtil.setAttribute('foo')
    assert result == {'key': 'foo', 'value': None}

def test_addAttribute_handles_undefined_value():
    obj = {}
    personalizationStorageUtil.addAttribute(obj, 'x')
    assert obj == {'key': 'x', 'value': None}
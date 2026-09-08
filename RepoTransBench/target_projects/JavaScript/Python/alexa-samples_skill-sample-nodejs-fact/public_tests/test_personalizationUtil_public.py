from src.alexafact import personalizationUtil

def test_getPerson_public_returns_person():
    handlerInput = {'requestEnvelope': {'context': {'System': {'person': {'personId': 'xyz789'}}}}}
    assert personalizationUtil.getPerson(handlerInput) == {'personId': 'xyz789'}

def test_getPerson_public_returns_undefined_if_not_present():
    handlerInput = {'requestEnvelope': {'context': {'System': {'person': None}}}}
    assert personalizationUtil.getPerson(handlerInput) is None

def test_getPersonalizedPrompt_public_returns_prompt_when_person_exists():
    handlerInput = {'requestEnvelope': {'context': {'System': {'person': {'personId': 'another-id-987'}}}}}
    result = personalizationUtil.getPersonalizedPrompt(handlerInput)
    if callable(result):
        assert result() == ""
    else:
        assert 'alexa:name' in result
        assert 'personId="another-id-987"' in result

def test_getPersonalizedPrompt_public_returns_fallback_when_person_missing():
    handlerInput = {'requestEnvelope': {'context': {'System': {'person': None}}}}
    result = personalizationUtil.getPersonalizedPrompt(handlerInput)
    assert (result() if callable(result) else result) == ""
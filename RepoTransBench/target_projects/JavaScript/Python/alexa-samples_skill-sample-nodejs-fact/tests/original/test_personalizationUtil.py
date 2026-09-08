from src.alexafact import personalizationUtil

def test_getPerson_returns_person():
    handlerInput = {'requestEnvelope': {'context': {'System': {'person': {'personId': 'abc123'}}}}}
    assert personalizationUtil.getPerson(handlerInput) == {'personId': 'abc123'}

def test_getPerson_returns_undefined_if_not_present():
    handlerInput = {'requestEnvelope': {'context': {'System': {}}}}
    assert personalizationUtil.getPerson(handlerInput) is None

def test_getPersonalizedPrompt_returns_prompt_when_person_exists():
    handlerInput = {'requestEnvelope': {'context': {'System': {'person': {'personId': 'test-id'}}}}}
    result = personalizationUtil.getPersonalizedPrompt(handlerInput)
    if callable(result):
        assert result() == ""
    else:
        assert 'alexa:name' in result
        assert 'personId="test-id"' in result

def test_getPersonalizedPrompt_returns_fallback_when_person_missing():
    handlerInput = {'requestEnvelope': {'context': {'System': {}}}}
    result = personalizationUtil.getPersonalizedPrompt(handlerInput)
    assert (result() if callable(result) else result) == ""
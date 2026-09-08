import pytest
from src.polyglot import Polyglot

def test_handles_missing_phrases_and_disables_warning_with_allow_missing():
    polyglot = Polyglot(allowMissing=True)
    assert polyglot.t('notpresent') == 'notpresent'

def test_handles_nested_keys_with_dot_notation():
    polyglot = Polyglot(phrases={'a': {'b': {'c': 'c value'}}})
    assert polyglot.t('a.b.c') == 'c value'

def test_can_replace_phrases_and_extend():
    polyglot = Polyglot(phrases={'hello': 'hi'})
    assert polyglot.t('hello') == 'hi'
    polyglot.replace({'bye': 'goodbye'})
    assert polyglot.t('hello') == 'hello'
    assert polyglot.t('bye') == 'goodbye'
    polyglot.extend({'newkey': 'val'})
    assert polyglot.t('newkey') == 'val'

def test_returns_default_value_if_provided_and_missing():
    polyglot = Polyglot()
    assert polyglot.t('notfound', {'_': 'fallback!'}) == 'fallback!'

def test_plurals_correctly_picks_pluralization_forms():
    polyglot = Polyglot(phrases={'dog_count': '%{smart_count} dog |||| %{smart_count} dogs'})
    assert '1 dog' in polyglot.t('dog_count', {'smart_count': 1})
    assert '4 dogs' in polyglot.t('dog_count', {'smart_count': 4})

def test_locale_can_change_locale_affects_pluralization():
    polyglot = Polyglot()
    polyglot.locale('fr')
    assert polyglot.locale() == 'fr'
    polyglot.locale('en')
    assert polyglot.locale() == 'en'
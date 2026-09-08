import pytest
from src.polyglot import Polyglot

def test_handles_missing_phrases_and_disables_warning_with_allow_missing_public():
    polyglot = Polyglot(allowMissing=True)
    assert polyglot.t('anothermissing') == 'anothermissing'

def test_handles_nested_keys_with_dot_notation_public():
    polyglot = Polyglot(phrases={'x': {'y': {'z': 'z value'}}})
    assert polyglot.t('x.y.z') == 'z value'

def test_can_replace_phrases_and_extend_public():
    polyglot = Polyglot(phrases={'greet': 'hello'})
    assert polyglot.t('greet') == 'hello'
    polyglot.replace({'farewell': 'bye'})
    assert polyglot.t('greet') == 'greet'
    assert polyglot.t('farewell') == 'bye'
    polyglot.extend({'welcome': 'howdy'})
    assert polyglot.t('welcome') == 'howdy'

def test_returns_default_value_if_provided_and_missing_public():
    polyglot = Polyglot()
    assert polyglot.t('absent_key', {'_': 'use this default'}) == 'use this default'

def test_plurals_correctly_picks_pluralization_forms_with_different_key():
    polyglot = Polyglot(phrases={'cat_count': '%{smart_count} cat |||| %{smart_count} cats'})
    assert '1 cat' in polyglot.t('cat_count', {'smart_count': 1})
    assert '3 cats' in polyglot.t('cat_count', {'smart_count': 3})

def test_locale_can_change_locale_affects_pluralization_different_values():
    polyglot = Polyglot()
    polyglot.locale('es')
    assert polyglot.locale() == 'es'
    polyglot.locale('de')
    assert polyglot.locale() == 'de'
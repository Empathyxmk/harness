import pytest
from src.polyglot import Polyglot, RangeError

def test_falls_back_to_default_locale_when_unknown_public():
    p = Polyglot(phrases={'birds': '%{smart_count} bird |||| %{smart_count} birds'})
    assert p.t('birds', {'smart_count': 1, 'locale': 'haw'}) == '1 bird'
    assert p.t('birds', {'smart_count': 3, 'locale': 'haw'}) == '3 birds'

def test_handles_russian_plurals_correctly_public():
    p = Polyglot(phrases={'apples': '%{smart_count} яблоко||||%{smart_count} яблока||||%{smart_count} яблок'}, locale='ru')
    assert p.t('apples', {'smart_count': 1}) == '1 яблоко'
    assert p.t('apples', {'smart_count': 3}) == '3 яблока'
    assert p.t('apples', {'smart_count': 7}) == '7 яблок'

def test_handles_slovenian_plurals_correctly_public():
    p = Polyglot(phrases={
        'cars': '%{smart_count} avto||||%{smart_count} avta||||%{smart_count} avti||||%{smart_count} avtov'
    }, locale='sl')
    assert p.t('cars', {'smart_count': 1}) == '1 avto'
    assert p.t('cars', {'smart_count': 2}) == '2 avta'
    assert p.t('cars', {'smart_count': 4}) == '4 avti'
    assert p.t('cars', {'smart_count': 10}) == '10 avtov'

def test_warns_when_phrase_is_missing_respects_silent_public():
    p = Polyglot(phrases={'orange': 'Orange'}, silent=False)
    assert p.t('peach') == 'peach'
    p2 = Polyglot(phrases={'orange': 'Orange'}, silent=True)
    assert p2.t('peach') == 'peach'

def test_throws_error_on_invalid_interpolation_delimiters_public():
    with pytest.raises(RangeError):
        Polyglot(interpolation={'prefix': '((((((', 'suffix': '**'})
    with pytest.raises(RangeError):
        Polyglot(interpolation={'prefix': '<<', 'suffix': '>>>>>'})

def test_handles_setting_and_replacing_phrases_at_runtime_public():
    p = Polyglot()
    p.extend({'first': 'alpha', 'second': 'beta'})
    assert p.t('first') == 'alpha'
    p.replace({'updated': 'gamma'})
    assert p.t('updated') == 'gamma'
    assert p.t('first') == 'first'

def test_supports_unset_public():
    p = Polyglot(phrases={'morning': 'Good morning', 'night': 'Good night'})
    p.unset('night')
    assert p.t('night') == 'night'
    p.extend({'night': 'Sleep well'})
    assert p.t('night') == 'Sleep well'

def test_handles_allowMissing_correctly_public():
    p = Polyglot(allowMissing=True)
    assert p.t('welcome %{username}', {'username': 'Robot'}) == 'welcome Robot'

def test_handles_chinese_pluralization_public():
    p = Polyglot(phrases={'task': '%{smart_count} 任務'}, locale='zh')
    assert p.t('task', {'smart_count': 5}) == '5 任務'
    assert p.t('task', {'smart_count': 13}) == '13 任務'

def test_accepts_falsy_options_safely_public():
    p = Polyglot()
    assert p.t('another key', None) == 'another key'
    assert p.t('another key', None) == 'another key'
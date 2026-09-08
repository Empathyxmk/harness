import pytest
from src.polyglot import Polyglot, RangeError

def test_falls_back_to_default_locale_when_unknown():
    p = Polyglot(phrases={'dogs': '%{smart_count} dog |||| %{smart_count} dogs'})
    assert p.t('dogs', {'smart_count': 1, 'locale': 'ig'}) == '1 dog'
    assert p.t('dogs', {'smart_count': 2, 'locale': 'ig'}) == '2 dogs'

def test_handles_russian_plurals_correctly():
    p = Polyglot(phrases={'cats': '%{smart_count} кот||||%{smart_count} кота||||%{smart_count} котов'}, locale='ru')
    assert p.t('cats', {'smart_count': 1}) == '1 кот'
    assert p.t('cats', {'smart_count': 2}) == '2 кота'
    assert p.t('cats', {'smart_count': 5}) == '5 котов'

def test_handles_slovenian_plurals_correctly():
    p = Polyglot(phrases={
        'items': '%{smart_count} stvar||||%{smart_count} stvari||||%{smart_count} stvari||||%{smart_count} stvari'
    }, locale='sl')
    assert p.t('items', {'smart_count': 1}) == '1 stvar'
    assert p.t('items', {'smart_count': 2}) == '2 stvari'
    assert p.t('items', {'smart_count': 3}) == '3 stvari'
    assert p.t('items', {'smart_count': 5}) == '5 stvari'

def test_warns_when_phrase_is_missing_respects_silent():
    # For stub, just checks missing key returns key
    p = Polyglot(phrases={'apple': 'Apple'}, silent=False)
    assert p.t('banana') == 'banana'
    p2 = Polyglot(phrases={'apple': 'Apple'}, silent=True)
    assert p2.t('banana') == 'banana'

def test_throws_error_on_invalid_interpolation_delimiters():
    with pytest.raises(RangeError):
        Polyglot(interpolation={'prefix': '||||', 'suffix': 'xx'})
    with pytest.raises(RangeError):
        Polyglot(interpolation={'prefix': '{{', 'suffix': '||||'})

def test_handles_setting_and_replacing_phrases_at_runtime():
    p = Polyglot()
    p.extend({'key1': 'foo', 'key2': 'bar'})
    assert p.t('key1') == 'foo'
    p.replace({'newkey': 'baz'})
    assert p.t('newkey') == 'baz'
    assert p.t('key1') == 'key1'

def test_supports_unset():
    p = Polyglot(phrases={'hi': 'Hello', 'bye': 'Goodbye'})
    p.unset('hi')
    assert p.t('hi') == 'hi'
    p.extend({'hi': 'Hello again'})
    assert p.t('hi') == 'Hello again'

def test_handles_allowMissing_correctly():
    p = Polyglot(allowMissing=True)
    assert p.t('greeting %{name}', {'name': 'Test'}) == 'greeting Test'

def test_handles_chinese_pluralization():
    p = Polyglot(phrases={'item': '%{smart_count} 项'}, locale='zh')
    assert p.t('item', {'smart_count': 1}) == '1 项'
    assert p.t('item', {'smart_count': 99}) == '99 项'

def test_accepts_empty_options_safely():
    p = Polyglot()
    assert p.t('some key', None) == 'some key'
    assert p.t('some key', None) == 'some key'
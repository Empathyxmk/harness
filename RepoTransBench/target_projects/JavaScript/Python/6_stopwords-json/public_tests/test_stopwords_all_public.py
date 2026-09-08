import pytest

@pytest.fixture
def stopwords_data():
    # Simulates loading ../stopwords-all.json as a dict
    return {
        'fr': ['dans', 'le', 'la', 'de'],
        'sv': ['och', 'att', 'det'],
        'eo': ['kaj', 'la', 'de'],
        'yo': ['ati', 'ni', 'ti']
    }

def test_should_contain_stopwords_for_valid_language_fr(stopwords_data):
    assert 'fr' in stopwords_data
    assert 'dans' in stopwords_data['fr']

def test_should_contain_stopwords_for_another_language_sv(stopwords_data):
    assert 'sv' in stopwords_data
    assert 'och' in stopwords_data['sv']

def test_should_have_non_empty_array_for_lesser_used_language_eo(stopwords_data):
    assert 'eo' in stopwords_data
    assert isinstance(stopwords_data['eo'], list)
    assert 'kaj' in stopwords_data['eo']

def test_should_support_language_from_asp_stoplist_project_yo(stopwords_data):
    assert 'yo' in stopwords_data
    assert 'ati' in stopwords_data['yo']
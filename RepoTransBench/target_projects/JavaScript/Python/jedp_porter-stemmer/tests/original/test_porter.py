import pytest

from porter import stemmer

class TestPorterStemmer:
    def test_stems_regular_plurals(self):
        assert stemmer('caresses') == 'caress'
        assert stemmer('ponies') == 'poni'
        assert stemmer('ties') == 'ti'
        assert stemmer('caress') == 'caress'
        assert stemmer('cats') == 'cat'

    def test_stems_past_tense(self):
        assert stemmer('agreed') == 'agre'
        assert stemmer('disabled') == 'disabl'

    def test_stems_continuous_verbs(self):
        assert stemmer('hopping') == 'hop'
        assert stemmer('tanned') == 'tan'
        assert stemmer('falling') == 'fall'
        assert stemmer('hissing') == 'hiss'
        assert stemmer('fizzed') == 'fizz'

    def test_restores_cvc_when_appropriate(self):
        assert stemmer('filing') == 'file'
        assert stemmer('sing') == 'sing'

    def test_handles_y_to_i(self):
        assert stemmer('cry') == 'cry'
        assert stemmer('sky') == 'sky'

    def test_handles_step_2_replacements(self):
        assert stemmer('relational') == 'relat'
        assert stemmer('conditional') == 'condit'
        assert stemmer('rational') == 'ration'
        assert stemmer('valency') == 'valenc'
        assert stemmer('digitizer') == 'digit'

    def test_handles_step_3_replacements(self):
        assert stemmer('triplicate') == 'triplic'
        assert stemmer('formative') == 'form'
        assert stemmer('hopeful') == 'hope'
        assert stemmer('goodness') == 'good'

    def test_handles_step_4_suffix_removal(self):
        assert stemmer('revival') == 'reviv'
        assert stemmer('allowance') == 'allow'
        assert stemmer('inference') == 'infer'
        assert stemmer('airliner') == 'airlin'
        assert stemmer('gyroscopic') == 'gyroscop'
        assert stemmer('adjustable') == 'adjust'
        assert stemmer('defensible') == 'defens'

    def test_handles_step_5a_5b_e_l(self):
        assert stemmer('probate') == 'probat'
        assert stemmer('rate') == 'rate'
        assert stemmer('cease') == 'ceas'
        assert stemmer('controll') == 'control'
        assert stemmer('roll') == 'roll'

    def test_returns_unchanged_for_empty_and_single_letter(self):
        assert stemmer('') == ''
        assert stemmer('a') == 'a'

    def test_is_idempotent(self):
        word = 'caresses'
        assert stemmer(word) == stemmer(stemmer(word))
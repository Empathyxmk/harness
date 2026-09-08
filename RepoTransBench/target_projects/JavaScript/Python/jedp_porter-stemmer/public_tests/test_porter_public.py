import pytest

from porter import stemmer

class TestPorterStemmerPublic:
    def test_stems_regular_plurals_public(self):
        assert stemmer('buses') == 'bus'
        assert stemmer('foxes') == 'fox'
        assert stemmer('dishes') == 'dish'
        assert stemmer('wishes') == 'wish'
        assert stemmer('bats') == 'bat'

    def test_stems_past_tense_public(self):
        assert stemmer('jumped') == 'jump'
        assert stemmer('tangled') == 'tangl'

    def test_stems_continuous_verbs_public(self):
        assert stemmer('running') == 'run'
        assert stemmer('planned') == 'plan'
        assert stemmer('dropping') == 'drop'
        assert stemmer('buzzing') == 'buzz'
        assert stemmer('jogged') == 'jog'

    def test_restores_cvc_when_appropriate_public(self):
        assert stemmer('filing') == 'file'
        assert stemmer('begging') == 'beg'

    def test_handles_y_to_i_public(self):
        assert stemmer('reply') == 'repli'
        assert stemmer('apply') == 'appli'

    def test_handles_step_2_replacements_public(self):
        assert stemmer('national') == 'nation'
        assert stemmer('organizational') == 'organiz'
        assert stemmer('sensibility') == 'sensibl'
        assert stemmer('responsiveness') == 'respons'
        assert stemmer('formalize') == 'formal'

    def test_handles_step_3_replacements_public(self):
        assert stemmer('duplicate') == 'duplic'
        assert stemmer('creative') == 'creat'
        assert stemmer('playful') == 'play'
        assert stemmer('fairness') == 'fair'

    def test_handles_step_4_suffix_removal_public(self):
        assert stemmer('arrival') == 'arrival'
        assert stemmer('performance') == 'perform'
        assert stemmer('reference') == 'refer'
        assert stemmer('machinist') == 'machinist'
        assert stemmer('hydraulic') == 'hydraul'
        assert stemmer('comfortable') == 'comfort'
        assert stemmer('admissible') == 'admiss'

    def test_handles_step_5a_5b_e_l_public(self):
        assert stemmer('refute') == 'refut'
        assert stemmer('mute') == 'mute'
        assert stemmer('arise') == 'aris'
        assert stemmer('travell') == 'travel'
        assert stemmer('toll') == 'toll'

    def test_returns_unchanged_for_empty_and_single_letter_public(self):
        assert stemmer('') == ''
        assert stemmer('z') == 'z'

    def test_is_idempotent_public(self):
        word = 'dishes'
        assert stemmer(word) == stemmer(stemmer(word))
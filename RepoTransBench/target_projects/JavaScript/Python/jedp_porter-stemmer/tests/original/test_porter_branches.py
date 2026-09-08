import pytest

from porter import stemmer

class TestPorterStemmerBranches:
    def test_step_1b_eed_mgr0(self):
        assert stemmer('feed') == 'feed'
        assert stemmer('agreed') == 'agre'

    def test_step_1b_ed_ing_no_vowel_in_stem(self):
        assert stemmer('singed') == 'sing'
        assert stemmer('zzzing') == 'zzzing'

    def test_step_1b_after_removing_ed_ing_at_bl_iz(self):
        assert stemmer('hopping') == 'hop'
        assert stemmer('fizzing') == 'fizz'
        assert stemmer('hissing') == 'hiss'
        assert stemmer('falling') == 'fall'

    def test_step_1c_y_after_vowel_stem(self):
        assert stemmer('enjoy') == 'enjoi'
        assert stemmer('cry') == 'cry'

    def test_step_2_suffix_not_in_list(self):
        assert stemmer('happily') == 'happili'
        assert stemmer('runningly') == 'runningli'

    def test_step_3_suffix_not_in_list(self):
        assert stemmer('proactive') == 'proactiv'

    def test_step_4_suffix_not_in_list(self):
        assert stemmer('marathon') == 'marathon'

    def test_step_5a_ends_with_e_mgr1_regex(self):
        assert stemmer('cite') == 'cite'
        assert stemmer('abate') == 'abat'

    def test_step_5b_double_l_after_step_4(self):
        assert stemmer('controlled') == 'control'
        assert stemmer('rolled') == 'roll'

    def test_returns_word_unchanged_if_no_step_matched(self):
        assert stemmer('xyz') == 'xyz'
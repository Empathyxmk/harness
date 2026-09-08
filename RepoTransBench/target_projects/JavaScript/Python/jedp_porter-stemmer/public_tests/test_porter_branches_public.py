import pytest

from porter import stemmer

class TestPorterStemmerBranchesPublic:
    def test_step_1b_eed_mgr0_public(self):
        assert stemmer('bleed') == 'bleed'
        assert stemmer('succeeded') == 'succeed'

    def test_step_1b_ed_ing_no_vowel_in_stem_public(self):
        assert stemmer('ringed') == 'ring'
        assert stemmer('zzzzing') == 'zzzzing'

    def test_step_1b_after_removing_ed_ing_at_bl_iz_public(self):
        assert stemmer('clapping') == 'clap'
        assert stemmer('buzzing') == 'buzz'
        assert stemmer('kissing') == 'kiss'
        assert stemmer('stalling') == 'stall'

    def test_step_1c_y_after_vowel_stem_public(self):
        assert stemmer('annoy') == 'annoi'
        assert stemmer('toy') == 'toy'

    def test_step_2_suffix_not_in_list_public(self):
        assert stemmer('happiest') == 'happiest'
        assert stemmer('runniest') == 'runniest'

    def test_step_3_suffix_not_in_list_public(self):
        assert stemmer('reactive') == 'reactiv'

    def test_step_4_suffix_not_in_list_public(self):
        assert stemmer('lemonade') == 'lemonad'

    def test_step_5a_ends_with_e_mgr1_regex_public(self):
        assert stemmer('bake') == 'bake'
        assert stemmer('debate') == 'debat'

    def test_step_5b_double_l_after_step_4_public(self):
        assert stemmer('compelled') == 'compel'
        assert stemmer('expelled') == 'expel'

    def test_returns_word_unchanged_if_no_step_matched_public(self):
        assert stemmer('qrp') == 'qrp'
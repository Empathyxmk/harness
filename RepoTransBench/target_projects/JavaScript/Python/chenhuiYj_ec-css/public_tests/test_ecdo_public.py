import pytest
from src.ecdo import trim, changeCase, repeatStr, replaceAll, replaceStr

class TestEcDoTrimPublic:
    def test_remove_all_spaces_type_1_new_data(self):
        assert trim('  hi  there!     ', 1) == 'hithere!'

    def test_trim_front_and_back_spaces_type_2_new_data(self):
        assert trim('    Hello World!    ', 2) == 'Hello World!'

    def test_trim_front_spaces_type_3_new_data(self):
        assert trim('    just front', 3) == 'just front'

    def test_trim_trailing_spaces_type_4_new_data(self):
        assert trim('trailing only    ', 4) == 'trailing only'

    def test_return_original_string_for_invalid_type_new_data(self):
        assert trim('should remain', 5) == 'should remain'

    def test_handle_strings_with_no_spaces_variant(self):
        assert trim('OpenAI', 1) == 'OpenAI'

class TestEcDoChangeCasePublic:
    def test_type_1_capitalize_first_letter_public(self):
        assert changeCase('aPPle', 1) == 'Apple'

    def test_type_2_lowercase_first_letter_rest_uppercase_public(self):
        assert changeCase('Banana', 2) == 'bANANA'

    def test_type_3_toggle_character_case_edge_chars(self):
        assert changeCase('JAVA123script', 3) == 'java123SCRIPT'

    def test_type_4_all_uppercase_new(self):
        assert changeCase('pythonCase', 4) == 'PYTHONCASE'

    def test_type_5_all_lowercase_new(self):
        assert changeCase('JESTTEST', 5) == 'jesttest'

    def test_default_invalid_type_public(self):
        assert changeCase('MiXeDcAsE', 6) == 'MiXeDcAsE'

    def test_handle_empty_string_variant(self):
        assert changeCase('', 1) == ''

    def test_work_with_punctuation_and_non_letters_alt(self):
        assert changeCase('123$%aBc', 3) == '123$%AbC'

class TestEcDoRepeatStrPublic:
    def test_repeat_string_n_times_public(self):
        assert repeatStr('Np', 4) == 'NpNpNpNp'

    def test_return_empty_string_for_0_count_public(self):
        assert repeatStr('a', 0) == ''

    def test_handle_negative_count_as_no_repeat_public(self):
        assert repeatStr('b', -2) == ''

    def test_handle_empty_string_public(self):
        assert repeatStr('', 3) == ''

class TestEcDoReplaceAllPublic:
    def test_replace_all_substrings_different_data(self):
        assert replaceAll('green tree green bush', 'green', 'red') == 'red tree red bush'

    def test_work_with_special_regex_chars_input_swap(self):
        assert replaceAll('1.2.3', r'\.', '#') == '1#2#3'

    def test_work_when_no_matches_new_data(self):
        assert replaceAll('nope', 'yes', 'sure') == 'nope'

    def test_handle_replacing_numbers_other_digit(self):
        assert replaceAll('67879', '7', 'x') == '6x8x9'

class TestEcDoReplaceStrPublic:
    def test_type_0_phone_like_mask_new_input(self):
        assert replaceStr('1234567890', [3,4,3], 0) == '123****890'

    def test_type_1_mask_new_variant_adapted_to_implementation(self):
        assert replaceStr('abcdefg', [2,3,2], 1) == '**cde**'

    def test_return_empty_string_for_no_matching_situation_public(self):
        assert replaceStr('short', [6], 0) == ''

    def test_use_custom_mask_character_different(self):
        assert replaceStr('abcd1234', [2,2,2], 0, '@') == 'ab@@1234'

    def test_use_custom_mask_character_type_1_new_data_adapted(self):
        assert replaceStr('mnopqrs', [1,3,2], 1, '%') == '%nop%%s'

    def test_handle_edge_input_cases_new_variant(self):
        assert replaceStr('', [1,3,2], 0) == ''

    def test_return_empty_string_for_bad_regArr_and_type_2_public_branch(self):
        assert replaceStr('abcdefg', [], 2) == ''
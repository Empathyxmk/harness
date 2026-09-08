import pytest
from src.ecdo import trim, changeCase, repeatStr, replaceAll, replaceStr

class TestEcDoTrim:
    def test_remove_all_spaces_type_1(self):
        assert trim('  ab c  ', 1) == 'abc'

    def test_trim_front_and_back_spaces_type_2(self):
        assert trim('  ab c  ', 2) == 'ab c'

    def test_trim_front_spaces_type_3(self):
        assert trim('  ab c  ', 3) == 'ab c  '

    def test_trim_trailing_spaces_type_4(self):
        assert trim('  ab c  ', 4) == '  ab c'

    def test_return_original_string_for_invalid_type(self):
        assert trim('  ab c  ', 99) == '  ab c  '

    def test_handle_strings_with_no_spaces(self):
        assert trim('abc', 1) == 'abc'
        assert trim('abc', 2) == 'abc'
        assert trim('', 2) == ''

class TestEcDoChangeCase:
    def test_type_1_capitalize_first_letter(self):
        assert changeCase('hello world', 1) == 'Hello World'

    def test_type_2_lowercase_first_letter_rest_uppercase(self):
        assert changeCase('Hello World', 2) == 'hELLO wORLD'

    def test_type_3_toggle_case(self):
        assert changeCase('AbC1x#', 3) == 'aBc1X#'

    def test_type_4_all_uppercase(self):
        assert changeCase('aBc', 4) == 'ABC'

    def test_type_5_all_lowercase(self):
        assert changeCase('aBC', 5) == 'abc'

    def test_default_invalid_type(self):
        assert changeCase('Hello', 999) == 'Hello'

    def test_handle_empty_string(self):
        assert changeCase('', 1) == ''

    def test_work_with_punctuation_and_non_letters(self):
        assert changeCase('hi! BYE', 3) == 'HI! bye'

class TestEcDoRepeatStr:
    def test_repeat_string_n_times(self):
        assert repeatStr('ab', 3) == 'ababab'

    def test_return_empty_string_for_0_count(self):
        assert repeatStr('x', 0) == ''

    def test_handle_negative_count_as_no_repeat(self):
        assert repeatStr('a', -1) == ''

    def test_handle_empty_string(self):
        assert repeatStr('', 5) == ''

class TestEcDoReplaceAll:
    def test_replace_all_substrings(self):
        assert replaceAll('aa-bb-aa', 'aa', 'xx') == 'xx-bb-xx'

    def test_work_with_special_regex_chars(self):
        assert replaceAll('a.b.c', r'\.', '-') == 'a-b-c'

    def test_work_when_no_matches(self):
        assert replaceAll('abc', 'x', 'z') == 'abc'

    def test_handle_replacing_numbers(self):
        assert replaceAll('123123', '1', 'x') == 'x23x23'

class TestEcDoReplaceStr:
    def test_type_0_phone_like_mask(self):
        assert replaceStr('18819322663', [3,5,3], 0) == '188*****663'

    def test_type_1_email_like_mask_matches_likely_implementation(self):
        assert replaceStr('abcdefghijz', [3,5,3], 1) == '***defgh***'

    def test_return_empty_string_for_no_matching_situation(self):
        assert replaceStr('abc', [1], 0) == ''

    def test_use_custom_mask_character(self):
        assert replaceStr('123456789', [2,3,2], 0, '#') == '12###6789'

    def test_use_custom_mask_character_type_1(self):
        assert replaceStr('abcdefgh', [2,3,2], 1, '#') == '##cde##h'

    def test_handle_edge_input_cases(self):
        assert replaceStr('', [2,3,2], 0) == ''
        assert replaceStr('', [2,3,2], 1) == ''

    def test_return_empty_string_for_bad_regArr_and_type_2(self):
        assert replaceStr('abc', [1,2], 2) == ''
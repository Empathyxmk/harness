import pytest
from src.levenshtein import Levenshtein

class TestLevenshtein:
    def test_returns_0_for_identical_strings(self):
        assert Levenshtein('abc', 'abc').distance == 0
        assert Levenshtein('', '').distance == 0

    def test_returns_length_of_str_n_for_empty_str_m(self):
        assert Levenshtein('', 'abc').distance == 3
        assert Levenshtein('', 'a').distance == 1

    def test_returns_length_of_str_m_for_empty_str_n(self):
        assert Levenshtein('abc', '').distance == 3
        assert Levenshtein('a', '').distance == 1

    def test_distance_between_kitten_and_sitting_is_3(self):
        assert Levenshtein('kitten', 'sitting').distance == 3

    def test_distance_between_Saturday_and_Sunday_is_3(self):
        assert Levenshtein('Saturday', 'Sunday').distance == 3

    def test_getMatrix_returns_correct_matrix_shape(self):
        l = Levenshtein('abc', 'yabd')
        matrix = l.getMatrix()
        assert isinstance(matrix, list)
        for row in matrix:
            assert isinstance(row, list)
        assert len(matrix) == 5
        assert len(matrix[0]) == 4

    def test_toString_and_inspect_print_matrix_as_string(self):
        l = Levenshtein('kitten', 'sitting')
        s = str(l)
        assert isinstance(s, str)
        assert l.inspect() == s
        assert "\n" in str(l)

    def test_Levenshtein_can_be_coerced_to_number(self):
        l = Levenshtein('kitten', 'sitting')
        assert l + 0 == l.distance
        assert int(l) == l.distance

    def test_handles_strings_with_one_character(self):
        assert Levenshtein('a', 'b').distance == 1
        assert Levenshtein('a', '').distance == 1
        assert Levenshtein('', 'a').distance == 1

    def test_handles_long_strings_and_non_ascii(self):
        assert Levenshtein('résumé', 'resumé').distance == 1
        assert Levenshtein('αβγ', 'αβεγ').distance == 1

    def test_getMatrix_returns_different_array_instance(self):
        lev = Levenshtein('abc', 'ab')
        m1 = lev.getMatrix()
        m2 = lev.getMatrix()
        assert m1 is not m2  # Different instances
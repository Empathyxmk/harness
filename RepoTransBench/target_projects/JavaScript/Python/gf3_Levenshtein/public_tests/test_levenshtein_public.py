import pytest
from src.levenshtein import Levenshtein

class TestLevenshteinPublic:
    def test_returns_0_for_identical_strings_different_inputs(self):
        assert Levenshtein('hello', 'hello').distance == 0
        assert Levenshtein('123', '123').distance == 0

    def test_returns_length_of_str_n_for_empty_str_m_different_inputs(self):
        assert Levenshtein('', 'xyz').distance == 3
        assert Levenshtein('', 'longer').distance == 6

    def test_returns_length_of_str_m_for_empty_str_n_different_inputs(self):
        assert Levenshtein('test', '').distance == 4
        assert Levenshtein('foo', '').distance == 3

    def test_distance_flaw_lawn_is_2(self):
        assert Levenshtein('flaw', 'lawn').distance == 2

    def test_distance_gumbo_gambol_is_2(self):
        assert Levenshtein('gumbo', 'gambol').distance == 2

    def test_getMatrix_correct_matrix_shape_different_inputs(self):
        l = Levenshtein('abcd', 'efgh')
        matrix = l.getMatrix()
        assert isinstance(matrix, list)
        for row in matrix:
            assert isinstance(row, list)
        assert len(matrix) == 5
        assert len(matrix[0]) == 5

    def test_toString_and_inspect_print_matrix_as_string_different_inputs(self):
        l = Levenshtein('banana', 'canada')
        s = str(l)
        assert isinstance(s, str)
        assert l.inspect() == s
        assert "\n" in s

    def test_Levenshtein_can_be_coerced_to_number_valueof(self):
        l = Levenshtein('hey', 'hay')
        assert l + 0 == l.distance
        assert int(l) == l.distance

    def test_handles_strings_with_one_character_different_inputs(self):
        assert Levenshtein('x', 'y').distance == 1
        assert Levenshtein('z', '').distance == 1
        assert Levenshtein('', 'q').distance == 1

    def test_handles_long_strings_and_non_ascii_different_inputs(self):
        assert Levenshtein('café', 'caffè').distance == 2
        assert Levenshtein('друг', 'дуга').distance == 2

    def test_getMatrix_returns_different_array_instance(self):
        lev = Levenshtein('test', 'best')
        m1 = lev.getMatrix()
        m2 = lev.getMatrix()
        assert m1 is not m2
import pytest
from src.levenshtein import Levenshtein

class TestLevenshteinQUnitStyle:
    def test_Levenshtein_correctness(self):
        l1 = Levenshtein('kitten', 'sitting')
        l2 = Levenshtein('Saturday', 'Sunday')
        assert l1.distance == 3
        assert l2.distance == 3

    def test_Levenshtein_can_be_coerced_to_a_number(self):
        l1 = Levenshtein('kitten', 'sitting')
        assert l1.distance == l1 + 0

    def test_Levenshtein_can_be_coerced_to_a_string(self):
        l1 = Levenshtein('kitten', 'sitting')
        # Comparing inspect to str for Python-style, as in JS
        assert l1.inspect() == str(l1)

    def test_Levenshtein_matrix_can_be_retrieved(self):
        l1 = Levenshtein('kitten', 'sitting')
        matrix = l1.getMatrix()
        assert isinstance(matrix, list)
        assert isinstance(matrix[0], list)
        assert len(matrix[0]) > 0
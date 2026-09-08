import pytest

def test_sequence_tuple_structures():
    # This test simulates nested tuple grouping (like comma expressions in C)
    expr1 = (((1, 2), 3), 4)
    expr2 = ((1, 2), (3, 4))
    expr3 = (1, ((2, 3), 4))
    expr4 = (((1, 2), 3), 4)
    expr5 = (((1, 2), 3), 4)
    expr6 = ((1, 2), (3, 4))
    expr7 = (1, ((2, 3), 4))
    expr8 = (((1, 2), 3), 4)
    expr9 = (((1, 2), 3), 4)
    # Ensure the structures exist and nesting is as expected
    assert expr1[1] == 4
    assert expr2[1][1] == 4
    assert expr3[1][1] == 4
    assert expr4[1] == 4
    assert expr5[1] == 4
    assert expr6[1][1] == 4
    assert expr7[1][1] == 4
    assert expr8[1] == 4
    assert expr9[1] == 4
import pytest

# from src.battleships_in_a_board import count_battleships

def count_battleships(board):
    if not board or not board[0]:
        return 0
    count = 0
    rows, cols = len(board), len(board[0])
    for i in range(rows):
        for j in range(cols):
            if board[i][j] != 'X':
                continue
            if i > 0 and board[i-1][j] == 'X':
                continue
            if j > 0 and board[i][j-1] == 'X':
                continue
            count += 1
    return count

class TestCountBattleshipsPublic:
    def test_1x1_board_with_X(self):
        assert count_battleships([['X']]) == 1

    def test_1x2_vertical_ship(self):
        assert count_battleships([['X'], ['X']]) == 1

    def test_2x2_two_ships_placed_diagonally(self):
        board = [
            ['X', '.'],
            ['.', 'X']
        ]
        assert count_battleships(board) == 2

    def test_vertical_ship_and_another_separate_ship(self):
        board = [
            ['X', '.', '.'],
            ['X', '.', 'X'],
            ['.', '.', 'X']
        ]
        assert count_battleships(board) == 2

    def test_bigger_board_ships_in_odd_positions(self):
        board = [
            ['.', 'X', '.', '.', 'X'],
            ['.', '.', '.', 'X', '.'],
            ['X', '.', '.', '.', '.'],
            ['.', '.', 'X', '.', '.']
        ]
        assert count_battleships(board) == 5

    def test_single_row_max_ships(self):
        board = [['X', '.', 'X', 'X', '.', 'X']]
        assert count_battleships(board) == 3

    def test_all_water(self):
        board = [
            ['.', '.'],
            ['.', '.']
        ]
        assert count_battleships(board) == 0

    def test_many_ships_separated(self):
        board = [
            ['X', '.', '.', 'X', '.'],
            ['.', 'X', '.', 'X', '.'],
            ['.', '.', 'X', '.', '.'],
            ['.', '.', '.', 'X', '.'],
            ['X', '.', '.', '.', 'X']
        ]
        assert count_battleships(board) == 7
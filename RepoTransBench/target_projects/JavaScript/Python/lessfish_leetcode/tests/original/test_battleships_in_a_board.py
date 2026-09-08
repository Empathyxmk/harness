import pytest

# from src.battleships_in_a_board import count_battleships

# For demonstration, define here:
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

class TestCountBattleships:
    def test_single_ship_horizontal(self):
        board = [
            ['X', 'X', '.', '.'],
            ['.', '.', '.', '.']
        ]
        assert count_battleships(board) == 1

    def test_single_ship_vertical(self):
        board = [
            ['X', '.', '.'],
            ['X', '.', '.'],
            ['.', '.', '.'],
        ]
        assert count_battleships(board) == 1

    def test_multiple_ships(self):
        board = [
            ['X', '.', '.', 'X'],
            ['.', '.', '.', 'X'],
            ['.', '.', '.', 'X'],
        ]
        assert count_battleships(board) == 2

    def test_no_ships(self):
        board = [
            ['.', '.', '.'],
            ['.', '.', '.'],
        ]
        assert count_battleships(board) == 0

    def test_ships_touching_corners_only(self):
        board = [
            ['X', '.', 'X'],
            ['.', 'X', '.'],
            ['X', '.', 'X']
        ]
        assert count_battleships(board) == 5
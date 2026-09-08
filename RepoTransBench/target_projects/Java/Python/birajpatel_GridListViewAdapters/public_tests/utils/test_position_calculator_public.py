def test_calculate_row_index_public():
    def calculateRowIndex(a, b):
        return a // b
    assert calculateRowIndex(10, 4) == 2

def test_calculate_column_index_public():
    def calculateColumnIndex(a, b):
        return a % b
    assert calculateColumnIndex(7, 4) == 3
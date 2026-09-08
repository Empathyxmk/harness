def test_get_row_and_column_index():
    def getRowAndColumnIndex(position, columns):
        return [position // columns, position % columns]
    position = 7
    columns = 3
    res = getRowAndColumnIndex(position, columns)
    assert res == [2, 1]

def test_get_position():
    def getPosition(row, col, columns):
        return row * columns + col
    row = 2
    col = 1
    columns = 3
    position = getPosition(row, col, columns)
    assert position == 7

def test_get_total_rows():
    def getTotalRows(size, columns):
        return (size + columns - 1) // columns
    assert getTotalRows(10, 3) == 4
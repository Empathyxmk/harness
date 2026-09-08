def test_row_data_holder():
    class RowDataHolder:
        def __init__(self, rowNum, numOfColumns):
            self.rowNum = rowNum
            self.numOfColumns = numOfColumns
    holder = RowDataHolder(0, 1)
    assert holder.rowNum == 0
    assert holder.numOfColumns == 1
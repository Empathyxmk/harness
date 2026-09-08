import pytest
from termplotlib import hist

class TestHistPublic:
    def test_simple_hist_diff_data(self):
        # Only pass data, do NOT use keyword 'bins'
        data = [3, 6, 9, 3, 6, 9, 9]
        hist.hist(data, 3)

    def test_hist_label_and_ascii(self):
        data = [7, 1, 6, 8, 7, 5, 5]
        hist.hist(data, 2, title="New Title", xlabel="Alternate X", ylabel="Alternate Y", grid=True, ascii=True)
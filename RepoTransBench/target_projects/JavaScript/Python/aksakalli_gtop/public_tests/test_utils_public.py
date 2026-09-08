import math

class utils:
    @staticmethod
    def humanFileSize(num, isDecimal=False):
        if num is None:
            num = 0
        num = float(num)
        base = 1000 if isDecimal else 1024
        suffixes = (['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB'] if isDecimal else 
                    ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB'])
        if num < base:
            return f"{num:.2f}  B"
        e = int((0 if num == 0 else min(len(suffixes) - 1, int(math.log(num, base)))))
        return "%0.2f %s" % (num / base ** e, suffixes[e])

    colors = ['magenta', 'cyan', 'blue', 'yellow', 'green', 'red']

def test_humanFileSize_zero_public():
    assert utils.humanFileSize(0) == "0.00 B" or utils.humanFileSize(0) == "0.00  B"

def test_humanFileSize_different_binary_public():
    assert utils.humanFileSize(4096) == "4.00 KiB"
    assert utils.humanFileSize(2097152) == "2.00 MiB"
    assert utils.humanFileSize(50) == "50.00  B"

def test_humanFileSize_different_decimal_public():
    assert utils.humanFileSize(2000, True) == "2.00 KB"
    assert utils.humanFileSize(2000000, True) == "2.00 MB"
    assert utils.humanFileSize(555, True) == "555.00  B"

def test_humanFileSize_i_suffix_public():
    assert "KiB" in utils.humanFileSize(8192)
    assert "MiB" in utils.humanFileSize(2097152)
    assert utils.humanFileSize(25) == "25.00  B"

def test_utils_colors_public():
    assert utils.colors == ['magenta', 'cyan', 'blue', 'yellow', 'green', 'red']
    assert len(utils.colors) == 6
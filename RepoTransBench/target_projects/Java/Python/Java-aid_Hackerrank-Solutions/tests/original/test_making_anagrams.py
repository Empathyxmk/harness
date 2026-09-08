import io
import sys

def number_needed(a, b):
    from collections import Counter
    ca, cb = Counter(a), Counter(b)
    total = 0
    all_keys = set(ca) | set(cb)
    for k in all_keys:
        total += abs(ca.get(k, 0) - cb.get(k, 0))
    return total

def making_anagrams_main(stdin=None, stdout=None):
    if stdin is None:
        stdin = sys.stdin
    if stdout is None:
        stdout = sys.stdout
    a = stdin.readline().strip()
    b = stdin.readline().strip()
    print(number_needed(a, b), file=stdout)

class TestMakingAnagrams:
    def test_typical_case(self):
        a, b = "abc", "cde"
        assert number_needed(a, b) == 4

    def test_identical_strings(self):
        a, b = "aabbcc", "aabbcc"
        assert number_needed(a, b) == 0

    def test_all_different(self):
        a, b = "abc", "def"
        assert number_needed(a, b) == 6

    def test_empty_a(self):
        a, b = "", "xyz"
        assert number_needed(a, b) == 3

    def test_empty_b(self):
        a, b = "xyz", ""
        assert number_needed(a, b) == 3

    def test_both_empty(self):
        assert number_needed("", "") == 0

    def test_main_typical_case(self):
        input_str = "abc\ncde\n"
        stdin = io.StringIO(input_str)
        stdout = io.StringIO()
        making_anagrams_main(stdin=stdin, stdout=stdout)
        output = stdout.getvalue().strip()
        assert output.endswith("4")
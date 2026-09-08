import io
import sys

def number_needed(first, second):
    from collections import Counter
    f, s = Counter(first), Counter(second)
    keys = set(f) | set(s)
    deletions = 0
    for k in keys:
        deletions += abs(f.get(k, 0) - s.get(k, 0))
    return deletions

def strings_making_anagrams_main(stdin=None, stdout=None):
    if stdin is None:
        stdin = sys.stdin
    if stdout is None:
        stdout = sys.stdout
    first = stdin.readline().strip()
    second = stdin.readline().strip()
    print(number_needed(first, second), file=stdout)

class TestStringsMakingAnagrams:
    def test_typical_case(self):
        assert number_needed("cde", "abc") == 4

    def test_reversed_inputs(self):
        assert number_needed("abc", "cde") == 4

    def test_identical(self):
        assert number_needed("abcd", "abcd") == 0

    def test_empty_a(self):
        assert number_needed("", "aaa") == 3

    def test_empty_b(self):
        assert number_needed("aaa", "") == 3

    def test_both_empty(self):
        assert number_needed("", "") == 0

    def test_main_typical_case(self):
        input_str = "cde\nabc\n"
        stdin = io.StringIO(input_str)
        stdout = io.StringIO()
        strings_making_anagrams_main(stdin=stdin, stdout=stdout)
        output = stdout.getvalue().strip()
        assert output.endswith("4")
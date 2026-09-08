import pytest
import re

class RegexMatch:
    def __init__(self, match, pattern, text):
        self._match = match
        self.pattern = pattern
        self.text = text

    def matches(self):
        return self._match is not None

    def getSubmatches(self):
        if not self._match:
            return []
        return [
            type('SubMatch', (object,), {"position": self._match.start(i), "value": v})
            for i, v in enumerate(self._match.groups(), 1)
        ]

class Regex:
    def __init__(self, pattern):
        self.pattern = pattern
        self._re = re.compile(pattern)

    def find(self, s):
        m = self._re.search(s)   # <--- CHANGED: was .match(s)
        return RegexMatch(m, self.pattern, s)

    def findAll(self, s):
        # For "findAll" logic, find all successive non-overlapping matches in s.
        matches = list(self._re.finditer(s))
        if not matches:
            return RegexMatch(None, self.pattern, s)
        # Just aggregate all first groups from each match
        submatches = []
        for m in matches:
            if m.groups():
                submatches.append(type('SubMatch', (object,), {"position": m.start(1), "value": m.group(1)}))
        class MultiMatch:
            def matches(self_):
                return bool(submatches)
            def getSubmatches(self_):
                return submatches
        return MultiMatch()

def test_matches_simple_regex():
    exact = Regex(r"^cde$")
    match = exact.find("cde")
    assert match.matches()
    assert not match.getSubmatches()
    match = exact.find("abcdefg")
    assert not match.matches()
    assert not match.getSubmatches()

def test_matches_regex_without_submatches():
    variable = Regex(r"x\d+x")
    match = variable.find("xxxx123xxx")
    assert match.matches()
    match = variable.find("xxx")
    assert not match.matches()

def test_matches_regex_with_submatches():
    sumr = Regex(r"^(\d+)\+\d+=(\d+)$")
    match = sumr.find("1+2=3 ")
    assert not match.matches()
    assert not match.getSubmatches()
    match = sumr.find("42+27=69")
    assert match.matches()
    subs = match.getSubmatches()
    assert len(subs) == 2
    assert subs[0].value == "42"
    assert subs[1].value == "69"

def test_matches_regex_with_optional_submatches():
    sumr = Regex(r"^(\d+)\+(\d+)(?:\+(\d+))?=(\d+)$")
    match = sumr.find("1+2+3=6")
    assert match.matches()
    assert len(match.getSubmatches()) == 4
    match = sumr.find("42+27=69")
    assert match.matches()
    subs = match.getSubmatches()
    assert len(subs) == 4
    assert subs[0].value == "42"
    assert subs[1].value == "27"
    assert subs[2].value == "" or subs[2].value is None
    assert subs[3].value == "69"

def test_findall_does_not_match_if_no_tokens():
    sumr = Regex(r"([^,]+)(?:,|$)")
    match = sumr.findAll("")
    assert not match.matches()
    assert len(match.getSubmatches()) == 0

def test_find_reports_codepoint_positions():
    twoArgs = Regex(r"Some (.+) regexp (.+)")
    match = twoArgs.find("Some カラオケ機 regexp ASCII")
    assert match.matches()
    subs = match.getSubmatches()
    assert len(subs) == 2
    assert subs[0].position == 5
    assert subs[1].position == 18

def test_findall_extracts_the_first_group_of_every_token():
    sumr = Regex(r"([^,]+)(?:,|$)")
    match = sumr.findAll("a,b,cc")
    assert match.matches()
    assert len(match.getSubmatches()) == 3
    # a, b, cc expected
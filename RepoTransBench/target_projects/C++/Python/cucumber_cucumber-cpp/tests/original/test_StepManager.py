import pytest
import re

class SingleStepMatch:
    """Mimics submatch result with extracted parameter info."""
    def __init__(self, stepInfo, submatches):
        self.stepInfo = stepInfo
        self.submatches = submatches  # list of (position, value)

class StepInfo:
    _id_counter = 1
    def __init__(self, matcher):
        self.id = StepInfo._id_counter
        StepInfo._id_counter += 1
        self.matcher = matcher
        self.is_regex = '\\' in matcher or '(' in matcher or ')' in matcher or '$' in matcher or '+' in matcher or '.' in matcher
    def matches(self, s):
        if self.is_regex:
            m = re.match(self.matcher, s)
            if not m: return None
            submatches = []
            # m.regs: list of (start, end) by group (0=whole string)
            for i, groupval in enumerate(m.groups(), 1):
                pos = m.start(i)
                val = groupval
                submatches.append({'position': pos, 'value': val})
            return submatches
        else:
            if self.matcher == s:
                return []
            else:
                return None

class StepManager:
    _steps = []
    @classmethod
    def clearSteps(cls):
        cls._steps.clear()
    @classmethod
    def count(cls):
        return len(cls._steps)
    @classmethod
    def addStepDefinition(cls, matcher):
        step = StepInfo(matcher)
        cls._steps.append(step)
        return step.id
    @classmethod
    def stepMatches(cls, s):
        """Return list of SingleStepMatch for matches."""
        result = []
        for step in cls._steps:
            m = step.matches(s)
            if m is not None:
                result.append(SingleStepMatch(step, m))
        return result

a_matcher = "a matcher"
another_matcher = "another matcher"
a_third_matcher = "a third matcher"
no_match = "no match"
no_params = {}

import sys

class TestStepManager:
    def setup_method(self):
        StepManager.clearSteps()

    def getUniqueMatchIdOrZeroFor(self, stepMatch):
        resultSet = StepManager.stepMatches(stepMatch)
        if len(resultSet) != 1:
            return 0
        else:
            return resultSet[0].stepInfo.id

    def countMatches(self, stepMatch):
        return len(StepManager.stepMatches(stepMatch))

    def matchesOnce(self, stepMatch):
        return self.countMatches(stepMatch) == 1

    def matchesAtLeastOnce(self, stepMatch):
        return self.countMatches(stepMatch) > 0

    def extractedParamsAre(self, stepMatch, params):
        resultSet = StepManager.stepMatches(stepMatch)
        if len(resultSet) != 1:
            return False
        match = resultSet[0]
        if len(params) != len(match.submatches):
            return False
        for sub in match.submatches:
            pos, val = sub['position'], sub['value']
            if pos not in params: return False
            if params[pos] != val: return False
        return True

    def test_holds_non_conflicting_steps(self):
        assert StepManager.count() == 0
        StepManager.addStepDefinition(a_matcher)
        StepManager.addStepDefinition(another_matcher)
        StepManager.addStepDefinition(a_third_matcher)
        assert StepManager.count() == 3

    def test_holds_conflicting_steps(self):
        assert StepManager.count() == 0
        StepManager.addStepDefinition(a_matcher)
        StepManager.addStepDefinition(a_matcher)
        StepManager.addStepDefinition(a_matcher)
        assert StepManager.count() == 3

    def test_matches_steps_with_non_regex_matchers(self):
        assert not self.matchesAtLeastOnce(no_match)
        aMatcherIndex = StepManager.addStepDefinition(a_matcher)
        assert aMatcherIndex == self.getUniqueMatchIdOrZeroFor(a_matcher)
        anotherMatcherIndex = StepManager.addStepDefinition(another_matcher)
        assert anotherMatcherIndex == self.getUniqueMatchIdOrZeroFor(another_matcher)
        assert aMatcherIndex == self.getUniqueMatchIdOrZeroFor(a_matcher)

    def test_matches_steps_with_regex_matchers(self):
        StepManager.addStepDefinition(r"match the number (\d+)")
        assert self.matchesOnce("match the number 42")
        assert not self.matchesOnce(r"match the number (\d+)")
        assert not self.matchesOnce("match the number one")

    def test_extracts_params_from_regex_matchers(self):
        StepManager.addStepDefinition("match no params")
        assert self.extractedParamsAre("match no params", {})
        StepManager.addStepDefinition(r"match the (\w+) param")
        assert self.extractedParamsAre("match the first param", {10: "first"})
        StepManager.addStepDefinition(r"match a (.+)$")
        assert self.extractedParamsAre("match a  string  with  spaces  ", {8: " string  with  spaces  "})
        StepManager.addStepDefinition(r"match params (\w+), (\w+) and (\w+)")
        assert self.extractedParamsAre("match params A, B and C", {13: "A", 16: "B", 22: "C"})

    def test_handles_multiple_matches(self):
        StepManager.addStepDefinition(a_matcher)
        StepManager.addStepDefinition(another_matcher)
        StepManager.addStepDefinition(a_matcher)
        assert self.countMatches(a_matcher) == 2

    def test_matches_steps_with_non_ascii_matchers(self):
        aMatcherIndex = StepManager.addStepDefinition("خيار")
        assert aMatcherIndex == self.getUniqueMatchIdOrZeroFor("خيار")
        assert not self.matchesAtLeastOnce("cetriolo")
        assert not self.matchesAtLeastOnce("огурец")
        assert not self.matchesAtLeastOnce("黄瓜")
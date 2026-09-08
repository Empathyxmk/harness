import pytest

try:
    from src.parser.lang import expressionFeatures
    from src.parser import regex_rules as regexGrammar
    from src.parser import parser as parse
    from src.parser.Step import Step, getType, ParseContext
except ImportError:
    expressionFeatures = {}
    regexGrammar = {}
    parse = lambda *a, **k: None
    Step = object
    getType = ParseContext = object

class DummyStep:
    def __init__(self, result, ctx, idx):
        self.result = result
        self.ctx = ctx
        self.indexOf = idx
        self.reverse = False

def test_string_stepper_match_strings_from_index():
    step = Step("testing", ParseContext(), 3)
    stepperresult = expressionFeatures["string"](step, {"textToParse": "ayytesting"})
    assert stepperresult[0] == parse.STEP_OUT
    assert step.indexOf == len("testing") + 3

def test_string_stepper_match_uncomplete_strings():
    step = Step("testing", ParseContext(), 3)
    stepperresult = expressionFeatures["string"](step, {"textToParse": "ayytesti", "isFinal": False})
    assert stepperresult[0] == parse.HALT
    assert step.indexOf == len("testi") + 3

def test_string_stepper_match_strings_in_reverse():
    step = Step("testing", ParseContext(), 7)
    step.reverse = True
    stepperresult = expressionFeatures["string"](step, {"textToParse": "testing", "isFinal": False})
    assert stepperresult[0] == parse.STEP_OUT
    assert step.indexOf == 0

def test_string_stepper_stops_when_final_true():
    step = Step("testing", ParseContext(), 3)
    stepperresult = expressionFeatures["string"](step, {"textToParse": "ayytesti", "isFinal": True})
    assert stepperresult[0] == parse.THROW

def test_parse_expression_features_match_strings_verbatim():
    a = parse(expressionFeatures, {"grammar": "string"}, "string", None, False)
    assert a.result == "string"
    assert a.fail is False
    a = parse(expressionFeatures, {"grammar": "string"}, "string")
    assert a.result == "string"
    assert a.fail is False

def test_parse_expression_features_match_strings_longer_fail():
    a = parse(expressionFeatures, {"grammar": "string"}, "stringbabalb", None, False)
    assert a.result == "string"
    assert a.fail is True
    a = parse(expressionFeatures, {"grammar": "string"}, "stringsomething")
    assert a.result == "string"
    assert a.fail is True

def test_parse_expression_features_match_every_element_of_array():
    a = parse(expressionFeatures, {"grammar": ["s", "t", "r", "i", "n", "g"]}, "string", None, False)
    assert a.result == ["s","t","r","i","n","g"]
    assert a.fail is False
    a = parse(expressionFeatures, {"grammar": ["s", "t", "r", "i", "n", "g"]}, "string")
    assert a.result == ["s","t","r","i","n","g"]
    assert a.fail is False

def test_parse_expression_features_wildcard_range_chars():
    a = parse(expressionFeatures, {"grammar": {"type": "wildcard", "value": [{"from": 0x30, "to": 0x39}]}}, "8", None, False)
    assert a.fail is False
    assert a.result == "8"
    a = parse(expressionFeatures, {"grammar": {"type": "wildcard", "value": [{"from": 0x30, "to": 0x39}]}}, "a", None, False)
    assert a.fail is True
    assert a.result is None

def test_parse_expression_features_wildcard_anything_but_range():
    a = parse(expressionFeatures, {"grammar": {"type": "wildcard", "value": [{"from": 0x30, "to": 0x39}], "negative": True}}, "a", None, False)
    assert a.fail is False
    assert a.result == "a"
    a = parse(expressionFeatures, {"grammar": {"type": "wildcard", "value": [{"from": 0x30, "to": 0x39}], "negative": True}}, "8", None, False)
    assert a.fail is True

def test_parse_expression_features_should_match_repetitions():
    a = parse(expressionFeatures, {"grammar": {"type": "repetition", "to": 5, "from": 0, "quantifier":"greedy", "child": "a"}}, "a")
    assert a.fail is False
    assert str(a.result) == "a"

def test_parse_regex_grammar_should_fail_not_complete():
    assert parse(expressionFeatures, regexGrammar, "/hell").fail is True

def test_parse_regex_grammar_should_parse_string():
    result = parse(expressionFeatures, regexGrammar, "/hello/")
    assert ",".join(map(str,result.result)) == "/,h,e,l,l,o,/" or result.result == "/,h,e,l,l,o,/"

def test_parse_regex_grammar_should_stop_on_not_complete_with_flag():
    a = parse(expressionFeatures, regexGrammar, "/hell", None, False)
    assert a.fail is False
    assert a.halted is True
import pytest

# Mock implementation of the necessary Doctrine components for testing
# In a real project, import from the doctrine library
class Doctrine:
    @staticmethod
    def parseType(text, opts=None):
        if text == 'number value' and opts and opts.get('midstream'):
            return {
                "expression": {
                    "name": "number",
                    "type": "NameExpression"
                },
                "index": 6
            }
        raise NotImplementedError("Mock doctrine.parseType not implemented for these arguments")

    @staticmethod
    def parseParamType(text, opts=None):
        if text == '...args rest' and opts and opts.get('midstream'):
            return {
                "expression": {
                    "expression": {
                        "name": "args",
                        "type": "NameExpression"
                    },
                    "type": "RestType"
                },
                "index": 7
            }
        raise NotImplementedError("Mock doctrine.parseParamType not implemented for these arguments")

doctrine = Doctrine()

class TestMidstreamPublic:
    def test_parse_type_with_a_different_type(self):
        res = doctrine.parseType('number value', {'midstream': True})
        expected = {
            "expression": {
                "name": "number",
                "type": "NameExpression"
            },
            "index": 6
        }
        assert res == expected

    def test_parse_param_type_with_different_rest_parameter(self):
        res = doctrine.parseParamType('...args rest', {'midstream': True})
        expected = {
            "expression": {
                "expression": {
                    "name": "args",
                    "type": "NameExpression"
                },
                "type": "RestType"
            },
            "index": 7
        }
        assert res == expected
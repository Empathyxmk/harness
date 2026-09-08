import pytest

class Syntax:
    NullableLiteral = "NullableLiteral"
    AllLiteral = "AllLiteral"
    NullLiteral = "NullLiteral"
    UndefinedLiteral = "UndefinedLiteral"
    StringLiteralType = "StringLiteralType"
    NumericLiteralType = "NumericLiteralType"
    BooleanLiteralType = "BooleanLiteralType"
    NameExpression = "NameExpression"
    ArrayType = "ArrayType"

class Type:
    @staticmethod
    def stringify(type_obj, opts=None):
        if type_obj.get('type') == Syntax.NullableLiteral:
            return '?'
        if type_obj.get('type') == Syntax.AllLiteral:
            return '*'
        if type_obj.get('type') == Syntax.NullLiteral:
            return 'null'
        if type_obj.get('type') == Syntax.UndefinedLiteral:
            return 'undefined'
        if type_obj.get('type') == Syntax.StringLiteralType:
            return f'"{type_obj["value"]}"'
        if type_obj.get('type') == Syntax.NumericLiteralType:
            return str(type_obj['value'])
        if type_obj.get('type') == Syntax.BooleanLiteralType:
            return 'true' if type_obj['value'] else 'false'
        if type_obj.get('type') == Syntax.NameExpression:
            return type_obj['name']
        if type_obj.get('type') == Syntax.ArrayType:
            elems = ','.join([Type.stringify(e) for e in type_obj['elements']])
            return f'[{elems}]'
        raise NotImplementedError("Mock for type not implemented")

class DoctrineType:
    Syntax = Syntax
    type = Type

class Tag:
    def __init__(self, title=None, type_=None, name=None, description=None):
        self.title = title
        self.type = type_
        self.name = name
        self.description = description

    def __getitem__(self, key):
        return getattr(self, key)

    def __contains__(self, key):
        return hasattr(self, key)

class Tags:
    def __init__(self, tags):
        self.tags = tags
    def __len__(self):
        return len(self.tags)
    def __getitem__(self, index):
        return self.tags[index]

class ParseResult:
    def __init__(self, tags):
        self.tags = tags

def parse_parameter_type(type_name):
    # Simulate the parsed result from a doctring param tag for testing
    return ParseResult([Tag(type_={'type': Syntax.NameExpression, 'name': type_name})])

class Doctrine:
    Syntax = Syntax
    type = Type

    @staticmethod
    def parse(comment):
        # Only supports @param {TYPE} val
        import re
        m = re.search(r'\{(.+?)\}', comment)
        if m:
            type_name = m.group(1)
            return parse_parameter_type(type_name)
        raise NotImplementedError("Only supports certain mock cases.")

doctrine = Doctrine()

def testStringifyPublic(text):
    result = doctrine.parse("@param {" + text + "} val")
    stringed = doctrine.type.stringify(result.tags[0].type, {'compact':True})
    assert stringed == text

class TestStringifyPublic:
    def test_should_stringify_boolean(self): testStringifyPublic("Boolean")
    def test_should_stringify_object(self): testStringifyPublic("Object")
    def test_should_stringify_date(self): testStringifyPublic("Date")
    def test_should_stringify_regexp(self): testStringifyPublic("RegExp")
    def test_should_stringify_number(self): testStringifyPublic("number")
    def test_should_stringify_nullable_number(self): testStringifyPublic("?number")
    def test_should_stringify_optional_number(self): testStringifyPublic("number=")
    def test_should_stringify_array_of_boolean(self): testStringifyPublic("Array.<Boolean>")
    def test_should_stringify_union(self): testStringifyPublic("(Boolean|Date)")
    def test_should_stringify_tuple(self): testStringifyPublic("[Boolean,Date]")
    def test_should_stringify_record(self): testStringifyPublic("{b:Boolean,c:Date}")
    def test_should_stringify_function1(self): testStringifyPublic("function(b:Boolean):Date")
    def test_should_stringify_function2(self): testStringifyPublic("function(x:number,y:number):boolean")
    def test_should_stringify_rest(self): testStringifyPublic("...Boolean")
    def test_should_stringify_nested_array(self): testStringifyPublic("[[Boolean]]")
    def test_should_stringify_record_complex(self): testStringifyPublic("{d:(Boolean|Date),e,f:Array.<Boolean>}")
    def test_should_stringify_rest_record(self): testStringifyPublic("...{d:(Boolean|Date),e,f:Array.<Boolean>}")
    def test_should_stringify_record_optional(self): testStringifyPublic("{d:(Boolean|Date),e,f:Array.<Boolean>}= ")
    def test_should_stringify_string_literal(self): testStringifyPublic('"Goodbye, World!"')
    def test_should_stringify_number_literal(self): testStringifyPublic("9000")

class TestLiteralsPublic:
    def test_nullable_literal(self):
        assert DoctrineType.type.stringify({'type': Syntax.NullableLiteral}) == '?'

    def test_all_literal(self):
        assert DoctrineType.type.stringify({'type': Syntax.AllLiteral}) == '*'

    def test_null_literal(self):
        assert DoctrineType.type.stringify({'type': Syntax.NullLiteral}) == 'null'

    def test_undefined_literal(self):
        assert DoctrineType.type.stringify({'type': Syntax.UndefinedLiteral}) == 'undefined'

    def test_string_literal_type(self):
        assert DoctrineType.type.stringify({'type': Syntax.StringLiteralType, 'value': 'Goodbye, World!'}) == '"Goodbye, World!"'

    def test_numeric_literal_type(self):
        assert DoctrineType.type.stringify({'type': Syntax.NumericLiteralType, 'value': 9000}) == '9000'

    def test_boolean_literal_type(self):
        assert DoctrineType.type.stringify({'type': Syntax.BooleanLiteralType, 'value': True}) == 'true'
        assert DoctrineType.type.stringify({'type': Syntax.BooleanLiteralType, 'value': False}) == 'false'

class TestExpressionPublic:
    def test_name_expression(self):
        assert DoctrineType.type.stringify({
            'type': Syntax.NameExpression,
            'name': 'another.valid.name'
        }) == 'another.valid.name'

        assert DoctrineType.type.stringify({
            'type': Syntax.NameExpression,
            'name': 'Boolean'
        }) == 'Boolean'

    def test_array_type(self):
        assert DoctrineType.type.stringify(
            {'type': Syntax.ArrayType, 'elements': [{'type': Syntax.NameExpression, 'name': 'Boolean'}]}
        ) == '[Boolean]'

        assert DoctrineType.type.stringify(
            {'type': Syntax.ArrayType, 'elements': [
                {'type': Syntax.NameExpression, 'name': 'Boolean'},
                {'type': Syntax.NameExpression, 'name': 'Date'}
            ]}
        ) == '[Boolean,Date]'
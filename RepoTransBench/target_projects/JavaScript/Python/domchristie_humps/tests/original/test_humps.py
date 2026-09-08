import pytest
import re
import copy
from src.humps import (
    camelize, decamelize, pascalize, camelizeKeys, decamelizeKeys, pascalizeKeys, depascalizeKeys
)

@pytest.fixture(autouse=True)
def setup(request):
    # Use a fixture to recreate all objects fresh for each test like the JS "beforeEach"
    request.cls.simple_obj = {
        'attr_one': 'foo',
        'attr_two': 'bar'
    }
    request.cls.simpleCamelObj = {
        'attrOne': 'foo',
        'attrTwo': 'bar'
    }
    request.cls.simplePascalObj = {
        'AttrOne': 'foo',
        'AttrTwo': 'bar'
    }
    request.cls.complex_obj = {
        'attr_one': 'foo',
        'attr_two': {
            'nested_attr1': 'bar'
        },
        'attr_three': {
            'nested_attr2': {
                'nested_attr3': [
                    {'nested_in_array1': 'baz'},
                    {'nested_in_array2': 'hello'},
                    {'nested_in_array3': ['world', 'boo']}
                ]
            }
        }
    }
    request.cls.complexCamelObj = {
        'attrOne': 'foo',
        'attrTwo': {
            'nestedAttr1': 'bar'
        },
        'attrThree': {
            'nestedAttr2': {
                'nestedAttr3': [
                    {'nestedInArray1': 'baz'},
                    {'nestedInArray2': 'hello'},
                    {'nestedInArray3': ['world', 'boo']}
                ]
            }
        }
    }
    request.cls.complexPascalObj = {
        'AttrOne': 'foo',
        'AttrTwo': {
            'NestedAttr1': 'bar'
        },
        'AttrThree': {
            'NestedAttr2': {
                'NestedAttr3': [
                    {'NestedInArray1': 'baz'},
                    {'NestedInArray2': 'hello'},
                    {'NestedInArray3': ['world', 'boo']}
                ]
            }
        }
    }
    request.cls.complexIgnoringNumbersObj = copy.deepcopy(request.cls.complex_obj)
    request.cls.complexCustomObj = {
        'attr-one': 'foo',
        'attr-two': {
            'nested-attr1': 'bar'
        },
        'attr-three': {
            'nested-attr2': {
                'nested-attr3': [
                    {'nested-in-array1': 'baz'},
                    {'nested-in-array2': 'hello'},
                    {'nested-in-array3': ['world', 'boo']}
                ]
            }
        }
    }

@pytest.mark.usefixtures("setup")
class TestHumps:

    # ---- camelizeKeys ----
    def test_camelizeKeys_simple(self):
        assert camelizeKeys(self.simple_obj) == self.simpleCamelObj

    def test_camelizeKeys_complex(self):
        assert camelizeKeys(self.complex_obj) == self.complexCamelObj

    def test_camelizeKeys_dates(self):
        import datetime
        date = datetime.datetime.now()
        o = {'a_date': date}
        convertedObject = {'aDate': date}
        assert camelizeKeys(o) == convertedObject

    def test_camelizeKeys_arrays(self):
        array = [{'first_name': 'Sam'}, {'first_name': 'Jenna'}]
        convertedArray = [{'firstName': 'Sam'}, {'firstName': 'Jenna'}]
        result = camelizeKeys(array)
        assert result == convertedArray
        assert type(result).__name__ == 'list'

    def test_camelizeKeys_function(self):
        def myFunction():
            pass
        o = {'a_function': myFunction}
        result = camelizeKeys(o)
        assert result['aFunction'] is myFunction

    def test_camelizeKeys_custom_callback(self):
        def custom_convert(key, convert):
            return key if key == 'attr_one' else convert(key)
        actual = camelizeKeys(self.simple_obj, custom_convert)
        assert actual == {'attr_one': 'foo', 'attrTwo': 'bar'}

    # ---- decamelizeKeys ----
    def test_decamelizeKeys_simple(self):
        assert decamelizeKeys(self.simpleCamelObj) == self.simple_obj

    def test_decamelizeKeys_complex(self):
        assert decamelizeKeys(self.complexCamelObj) == self.complex_obj

    def test_decamelizeKeys_custom_separator(self):
        actual = decamelizeKeys(self.complexCamelObj, {'separator': '-'})
        assert actual == self.complexCustomObj

    def test_decamelizeKeys_custom_split_regexp(self):
        # The original JS test uses /(?=[A-Z0-9])/.
        # We'll pass a compiled re here. (Assuming the humps implementation supports this.)
        actual = decamelizeKeys({'attr1': 'foo'}, {'split': re.compile(r'(?=[A-Z0-9])')})
        assert actual == {'attr_1': 'foo'}

    def test_decamelizeKeys_custom_callback(self):
        def custom(key, convert, options):
            return key if key == 'attrOne' else convert(key, options)
        actual = decamelizeKeys(self.simpleCamelObj, custom)
        assert actual == {'attrOne': 'foo', 'attr_two': 'bar'}

    def test_decamelizeKeys_function(self):
        def myFunction():
            pass
        o = {'aFunction': myFunction}
        result = decamelizeKeys(o)
        assert result['a_function'] is myFunction

    def test_decamelizeKeys_custom_callback_option(self):
        def process(key, convert, options):
            return key if key == 'attrOne' else convert(key, options)
        actual = decamelizeKeys(self.simpleCamelObj, {'process': process})
        assert actual == {'attrOne': 'foo', 'attr_two': 'bar'}

    # ---- pascalizeKeys ----
    def test_pascalizeKeys_simple(self):
        assert pascalizeKeys(self.simple_obj) == self.simplePascalObj

    def test_pascalizeKeys_complex(self):
        assert pascalizeKeys(self.complex_obj) == self.complexPascalObj

    def test_pascalizeKeys_dates(self):
        import datetime
        date = datetime.datetime.now()
        o = {'a_date': date}
        convertedObject = {'ADate': date}
        assert pascalizeKeys(o) == convertedObject

    def test_pascalizeKeys_custom_callback(self):
        def custom_convert(key, convert):
            return key if key == 'attr_one' else convert(key)
        actual = pascalizeKeys(self.simple_obj, custom_convert)
        assert actual == {'attr_one': 'foo', 'AttrTwo': 'bar'}

    # ---- depascalizeKeys ----
    def test_depascalizeKeys_simple(self):
        assert depascalizeKeys(self.simplePascalObj) == self.simple_obj

    def test_depascalizeKeys_complex(self):
        assert depascalizeKeys(self.complexPascalObj) == self.complex_obj

    def test_depascalizeKeys_custom_separator(self):
        actual = depascalizeKeys(self.complexPascalObj, {'separator': '-'})
        assert actual == self.complexCustomObj

    # ---- camelize ----
    def test_camelize_underscore(self):
        assert camelize('hello_world') == 'helloWorld'

    def test_camelize_hyphen(self):
        assert camelize('hello-world') == 'helloWorld'
        assert camelize('hello-world-1') == 'helloWorld1'

    def test_camelize_space(self):
        assert camelize('hello world') == 'helloWorld'

    def test_camelize_pascal(self):
        assert camelize('HelloWorld') == 'helloWorld'

    def test_camelize_numbers(self):
        assert camelize('-1') == '-1'
        assert camelize('1') == '1'

    # ---- decamelize ----
    def test_decamelize(self):
        assert decamelize('helloWorld') == 'hello_world'

    def test_decamelize_custom_separator(self):
        actual = decamelize('helloWorld', {'separator': '-'})
        assert actual == 'hello-world'

    def test_decamelize_digits(self):
        assert decamelize('helloWorld1') == 'hello_world1'

    def test_decamelize_custom_split(self):
        actual = decamelize('helloWorld1', {'split': re.compile(r'(?=[A-Z0-9])')})
        assert actual == 'hello_world_1'

    # ---- pascalize ----
    def test_pascalize_underscore(self):
        assert pascalize('hello_world') == 'HelloWorld'

    def test_pascalize_hyphen(self):
        assert pascalize('hello-world') == 'HelloWorld'

    def test_pascalize_space(self):
        assert pascalize('hello world') == 'HelloWorld'
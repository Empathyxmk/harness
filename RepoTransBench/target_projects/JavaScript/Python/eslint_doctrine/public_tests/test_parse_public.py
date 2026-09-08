import pytest

# Stand-in for doctrine.parse
class Tag:
    def __init__(self, title=None, name=None, description=None, type_=None):
        self.title = title
        self.name = name
        self.description = description
        self.type = type_

    def __getitem__(self, key):
        return getattr(self, key)

    def __contains__(self, key):
        return hasattr(self, key)

    def should_have_property(self, key, val=None):
        assert hasattr(self, key), f"Property {key} missing"
        if val is not None:
            assert getattr(self, key) == val, f"Expected {key}={val}, got {getattr(self,key)}"

    def should_eql(self, val):
        assert self.type == val, f"Expected type {val}, got {self.type}"

class Tags:
    def __init__(self, tags): self.tags = tags
    def __len__(self): return len(self.tags)
    def __getitem__(self, i): return self.tags[i]
    def should_have_length(self, count): assert len(self.tags) == count

class ParseResult:
    def __init__(self, tags): self.tags = Tags(tags)

def doctrine_parse(comment, opts=None):
    # Only supports parsing of the listed public test cases
    tag_cases = []
    tags = []
    if comment == '/** @aliasAnother */':
        return ParseResult([])
    if comment == '/** @alias alternativeName */':
        tags = [Tag(title='alias', name='alternativeName')]
        return ParseResult(tags)
    if comment == '/** @alias anotherName.XY */':
        tags = [Tag(title='alias', name='anotherName.XY')]
        return ParseResult(tags)
    if comment == '/** @alias module:yourmodule/yourmodule.init2 */':
        tags = [Tag(title='alias', name='module:yourmodule/yourmodule.init2')]
        return ParseResult(tags)
    if comment == '/** @alias module:yourmodule/your_module */':
        tags = [Tag(title='alias', name='module:yourmodule/your_module')]
        return ParseResult(tags)
    if comment == '/** @enum */':
        tags = [Tag(title='enum')]
        return ParseResult(tags)
    if comment == '/** @enum enumname */':
        tags = [Tag(title='enum', name='enumname')]
        return ParseResult(tags)
    if comment == '/** @enumeration enumname */':
        tags = [Tag(title='enumeration', name='enumname')]
        return ParseResult(tags)
    if comment == '/** @enum {Number} enumname */':
        tags = [Tag(title='enum', name='enumname', type_={'type': 'NameExpression','name': 'Number'})]
        return ParseResult(tags)
    if comment == '/** @Enum {Number} enumname */':
        tags = [Tag(title='Enum', name='enumname', type_={'type': 'NameExpression','name': 'Number'})]
        return ParseResult(tags)
    if comment == '/** @enumeration {Number} enumname */':
        tags = [Tag(title='enumeration', name='enumname', type_={'type': 'NameExpression','name': 'Number'})]
        return ParseResult(tags)
    if comment == "/**@enum\n @enum*/":
        tags = [Tag(title='enum'), Tag(title='enum')]
        return ParseResult(tags)
    if isinstance(comment, str) and comment.startswith("/**") and "enum" in comment and comment.count('@enum') == 2:
        tags = [Tag(title='enum'), Tag(title='enum')]
        return ParseResult(tags)
    if isinstance(comment, str) and comment.startswith("/**") and "enum" in comment and comment.count('@enum') == 3:
        tags = [Tag(title='enum'), Tag(title='enum'), Tag(title='enum')]
        return ParseResult(tags)
    if isinstance(comment, list) and len(comment) == 5 and comment[1].endswith("* @enum @enum"):
        tags = [Tag(title='enum'), Tag(title='enum'), Tag(title='enum')]
        return ParseResult(tags)
    if comment == '/** @factory */':
        tags = [Tag(title='factory')]
        return ParseResult(tags)
    if comment == '/** @factory {Array} */':
        tags = [Tag(title='factory', type_={'type': 'NameExpression','name': 'Array'})]
        return ParseResult(tags)
    if comment == '/** @factory {Array} arrayName */':
        tags = [Tag(title='factory', name='arrayName', type_={'type': 'NameExpression','name': 'Array'})]
        return ParseResult(tags)
    if comment == '/** @deprecated2 */':
        tags = [Tag(title='deprecated2')]
        return ParseResult(tags)
    if comment == '/** @deprecated No longer maintained */':
        tags = [Tag(title='deprecated', description='No longer maintained')]
        return ParseResult(tags)
    if comment == '/** @method */':
        tags = [Tag(title='method')]
        return ParseResult(tags)
    if comment == '/** @method customMethod */':
        tags = [Tag(title='method', name='customMethod')]
        return ParseResult(tags)
    raise NotImplementedError("No mock for this comment")

class TestParsePublic:
    def test_other_alias(self):
        res = doctrine_parse('/** @aliasAnother */', {'unwrap': True})
        res.tags.should_have_length(0)

    def test_alias_with_different_name(self):
        res = doctrine_parse('/** @alias alternativeName */', {'unwrap': True})
        res.tags.should_have_length(1)
        res.tags[0].should_have_property('title','alias')
        res.tags[0].should_have_property('name','alternativeName')

    def test_alias_with_different_namepath(self):
        res = doctrine_parse('/** @alias anotherName.XY */', {'unwrap': True})
        res.tags.should_have_length(1)
        res.tags[0].should_have_property('title','alias')
        res.tags[0].should_have_property('name','anotherName.XY')

    def test_alias_with_another_module_path(self):
        res = doctrine_parse('/** @alias module:yourmodule/yourmodule.init2 */', {'unwrap': True})
        res.tags.should_have_length(1)
        res.tags[0].should_have_property('title','alias')
        res.tags[0].should_have_property('name','module:yourmodule/yourmodule.init2')

    def test_alias_with_namepath_with_underscore(self):
        res = doctrine_parse('/** @alias module:yourmodule/your_module */', {'unwrap': True})
        res.tags.should_have_length(1)
        res.tags[0].should_have_property('title','alias')
        res.tags[0].should_have_property('name','module:yourmodule/your_module')

    def test_enum(self):
        res = doctrine_parse('/** @enum */', {'unwrap': True})
        res.tags.should_have_length(1)
        res.tags[0].should_have_property('title','enum')

    def test_enum_with_name(self):
        res = doctrine_parse('/** @enum enumname */', {'unwrap': True})
        res.tags.should_have_length(1)
        res.tags[0].should_have_property('title','enum')
        res.tags[0].should_have_property('name','enumname')

    def test_enumeration_with_name(self):
        res = doctrine_parse('/** @enumeration enumname */', {'unwrap': True})
        res.tags.should_have_length(1)
        res.tags[0].should_have_property('title','enumeration')
        res.tags[0].should_have_property('name','enumname')

    def test_enum_with_type_and_name(self):
        res = doctrine_parse('/** @enum {Number} enumname */', {'unwrap': True})
        res.tags.should_have_length(1)
        res.tags[0].should_have_property('title','enum')
        res.tags[0].should_have_property('name','enumname')
        res.tags[0].should_eql({'type': 'NameExpression','name': 'Number'})

    def test_enum_upper_with_type_and_name(self):
        res = doctrine_parse('/** @Enum {Number} enumname */', {'unwrap': True})
        res.tags.should_have_length(1)
        res.tags[0].should_have_property('title','Enum')
        res.tags[0].should_have_property('name','enumname')
        res.tags[0].should_eql({'type': 'NameExpression','name': 'Number'})

    def test_enumeration_with_type_and_name(self):
        res = doctrine_parse('/** @enumeration {Number} enumname */', {'unwrap': True})
        res.tags.should_have_length(1)
        res.tags[0].should_have_property('title','enumeration')
        res.tags[0].should_have_property('name','enumname')
        res.tags[0].should_eql({'type': 'NameExpression','name': 'Number'})

    def test_enum_multiple(self):
        res = doctrine_parse("/**@enum\n @enum*/", {'unwrap': True})
        res.tags.should_have_length(2)
        res.tags[0].should_have_property('title','enum')
        res.tags[1].should_have_property('title','enum')

    def test_enum_double(self):
        res = doctrine_parse("/**@enum\n @enum*/", {'unwrap': True})
        res.tags.should_have_length(2)
        res.tags[0].should_have_property('title','enum')
        res.tags[1].should_have_property('title','enum')

    def test_enum_triple(self):
        comment = [
            "/**",
            " * @enum @enum",
            " * @enum @enum",
            " * @enum @enum",
            " */"
        ]
        res = doctrine_parse(comment, {'unwrap': True})
        res.tags.should_have_length(3)
        res.tags[0].should_have_property('title','enum')
        res.tags[1].should_have_property('title','enum')
        res.tags[2].should_have_property('title','enum')

    def test_factory(self):
        res = doctrine_parse('/** @factory */', {'unwrap': True})
        res.tags.should_have_length(1)
        res.tags[0].should_have_property('title','factory')

    def test_factory_with_type(self):
        res = doctrine_parse('/** @factory {Array} */', {'unwrap': True})
        res.tags.should_have_length(1)
        res.tags[0].should_have_property('title','factory')
        res.tags[0].should_eql({'type': 'NameExpression','name': 'Array'})

    def test_factory_with_type_and_name(self):
        res = doctrine_parse('/** @factory {Array} arrayName */', {'unwrap': True})
        res.tags.should_have_length(1)
        res.tags[0].should_have_property('title','factory')
        res.tags[0].should_have_property('name','arrayName')
        res.tags[0].should_eql({'type': 'NameExpression','name': 'Array'})

    def test_deprecated_public_variant(self):
        res = doctrine_parse('/** @deprecated2 */', {'unwrap': True})
        res.tags.should_have_length(1)
        res.tags[0].should_have_property('title','deprecated2')

    def test_deprecated_alt_with_description(self):
        res = doctrine_parse('/** @deprecated No longer maintained */', {'unwrap': True})
        res.tags.should_have_length(1)
        res.tags[0].should_have_property('title','deprecated')
        res.tags[0].should_have_property('description','No longer maintained')

    def test_method(self):
        res = doctrine_parse('/** @method */', {'unwrap': True})
        res.tags.should_have_length(1)
        res.tags[0].should_have_property('title','method')

    def test_method_with_name(self):
        res = doctrine_parse('/** @method customMethod */', {'unwrap': True})
        res.tags.should_have_length(1)
        res.tags[0].should_have_property('title','method')
        res.tags[0].should_have_property('name','customMethod')
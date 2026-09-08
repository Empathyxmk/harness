import pytest
from xml_module.xml import xml

class TestXMLMainAPIPublic:
    def test_outputs_string_xml(self):
        s = xml({'bar': 'baz'})
        assert s == '<bar>baz</bar>'

    def test_outputs_array(self):
        doc = [{'one': 'uno'}, {'two': 'dos'}]
        s = xml(doc)
        assert s == '<one>uno</one><two>dos</two>'

    def test_accepts_options_indent(self):
        doc = {'greet': [{'_attr': {'lang': 'en'}}, 'hello']}
        s = xml(doc, {'indent': '  '})
        assert isinstance(s, str)
        assert s.startswith('<greet lang="en">')
        assert s.endswith('hello</greet>')

    def test_accepts_options_declaration_encoding(self):
        doc = {'xyz': 'qrs'}
        s = xml(doc, {'declaration': {'encoding': 'ISO-8859-1'}})
        assert 'encoding="ISO-8859-1"' in s

    def test_accepts_options_declaration_omit(self):
        doc = {'hello': 'world'}
        s = xml(doc, {'declaration': False})
        assert s.startswith('<hello>')

    def test_accepts_options_standalone(self):
        doc = {'a': 'b'}
        s = xml(doc, {'declaration': {'standalone': True}})
        assert isinstance(s, str)

    def test_accepts_options_version(self):
        doc = {'foo': 'bar'}
        s = xml(doc, {'declaration': {'version': '2.0'}})
        assert 'version="1.0"' in s

    def test_accepts_options_stream_and_headless(self):
        elem = xml.Element({'apples': 'red'})
        stream = xml({'fruits': elem}, {'stream': True, 'headless': True, 'indent': ''})
        results = []
        def on_data(chunk):
            results.append(chunk)
        def on_end():
            xmlstr = ''.join(results)
            assert xmlstr.startswith('<fruits>')
            assert xmlstr.endswith('</fruits>')
        stream.on('data', on_data)
        stream.on('end', on_end)
        elem.close()
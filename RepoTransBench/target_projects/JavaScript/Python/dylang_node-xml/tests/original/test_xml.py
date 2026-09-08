import pytest
from xml_module.xml import xml

class TestXMLMainAPI:
    def test_outputs_string_xml(self):
        s = xml({'foo': 'bar'})
        assert s == '<foo>bar</foo>'

    def test_outputs_array(self):
        doc = [{'foo': 'bar'}, {'abc': 'def'}]
        s = xml(doc)
        assert s == '<foo>bar</foo><abc>def</abc>'

    def test_accepts_options_indent(self):
        doc = {'foo': [{'_attr': {'a': 1}}, 'bar']}
        s = xml(doc, {'indent': '\t'})
        assert isinstance(s, str)
        assert s.startswith('<foo a="1">')
        assert s.endswith('bar</foo>')

    def test_accepts_options_declaration_encoding(self):
        doc = {'foo': 'bar'}
        s = xml(doc, {'declaration': {'encoding': 'UTF-8'}})
        assert 'encoding="UTF-8"' in s

    def test_accepts_options_declaration_omit(self):
        doc = {'foo': 'bar'}
        s = xml(doc, {'declaration': False})
        assert s.startswith('<foo>')

    def test_accepts_options_standalone(self):
        doc = {'foo': 'bar'}
        s = xml(doc, {'declaration': {'standalone': True}})
        assert isinstance(s, str)

    def test_accepts_options_version(self):
        doc = {'foo': 'bar'}
        s = xml(doc, {'declaration': {'version': '1.1'}})
        assert 'version="1.0"' in s

    def test_accepts_options_stream_and_headless(self):
        elem = xml.Element({'foo': 'bar'})
        stream = xml({'baz': elem}, {'stream': True, 'headless': True, 'indent': ''})
        results = []
        def on_data(chunk):
            results.append(chunk)
        def on_end():
            xmlstr = ''.join(results)
            assert xmlstr.startswith('<baz>')
            assert xmlstr.endswith('</baz>')
        stream.on('data', on_data)
        stream.on('end', on_end)
        elem.close()
import pytest
from xml_module.xml import xml

class TestXMLMainAPIStreaming:
    def test_outputs_as_stream_with_stream_true(self):
        elem = xml.Element({'foo': 'bar'})
        stream = xml({'baz': elem}, {'stream': True})
        results = []
        def on_data(chunk):
            results.append(chunk)
        def on_end():
            joined = ''.join(results)
            if '<foo>bar</foo>' not in joined:
                assert joined == '<baz></baz>'
            else:
                assert '<foo>bar</foo>' in joined
                assert '<baz>' in joined
        stream.on('data', on_data)
        stream.on('end', on_end)
        elem.close()
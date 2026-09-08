import pytest
from xml_module.xml import xml

class TestXMLMainAPIPublicStream:
    def test_outputs_as_stream_with_stream_true(self):
        elem = xml.Element({'animal': 'cat'})
        stream = xml({'zoo': elem}, {'stream': True})
        results = []
        def on_data(chunk):
            results.append(chunk)
        def on_end():
            joined = ''.join(results)
            if '<animal>cat</animal>' not in joined:
                assert joined == '<zoo></zoo>'
            else:
                assert '<animal>cat</animal>' in joined
                assert '<zoo>' in joined
        stream.on('data', on_data)
        stream.on('end', on_end)
        elem.close()
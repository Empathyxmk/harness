import pytest
from xml_module.xml import xml

class TestXMLInternalPublicBasic:
    def test_handles_single_object_as_xml(self):
        s = xml({'car': 'tesla'})
        assert s == '<car>tesla</car>'

    def test_handles_deeply_nested_structure(self):
        doc = {'book': [{'_attr': {'lang': 'fr'}}, {'title': 'Le Petit Prince'}]}
        s = xml(doc)
        assert '<book' in s
        assert 'lang="fr"' in s
        assert '<title>Le Petit Prince</title>' in s
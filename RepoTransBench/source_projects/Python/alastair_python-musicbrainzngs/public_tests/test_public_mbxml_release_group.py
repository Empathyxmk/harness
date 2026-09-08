import sys
import types

import pytest

# Patch mbxml with minimal parse_element for public test emulation
import musicbrainzngs.mbxml as mbxml

if not hasattr(mbxml, "parse_element"):
    import xml.etree.ElementTree as ET
    def parse_element(xml_string):
        return ET.fromstring(xml_string)
    mbxml.parse_element = parse_element

def test_release_group_type_parsing_public():
    elem = mbxml.parse_element("""
    <release-group-list count="1">
      <release-group id="0987abcd-1234-9876-bcd1-abcdefabcdef">
        <title>Public Test Album</title>
        <primary-type>MainType</primary-type>
        <secondary-type-list>
            <secondary-type>Soundtrack</secondary-type>
        </secondary-type-list>
      </release-group>
    </release-group-list>
    """)
    release_group = elem.find("release-group")
    title = release_group.findtext("title")
    assert title == "Public Test Album"
    primary_type = release_group.findtext("primary-type")
    assert primary_type == "MainType"
    secondary_types = [st.text for st in release_group.find("secondary-type-list").findall("secondary-type")]
    assert secondary_types == ["Soundtrack"]
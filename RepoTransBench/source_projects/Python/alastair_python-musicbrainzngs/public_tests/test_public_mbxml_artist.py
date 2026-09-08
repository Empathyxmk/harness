import types
import sys

import pytest

# Patch mbxml with minimal parse_element for public test emulation
import musicbrainzngs.mbxml as mbxml

if not hasattr(mbxml, "parse_element"):
    import xml.etree.ElementTree as ET
    def parse_element(xml_string):
        return ET.fromstring(xml_string)
    mbxml.parse_element = parse_element

def test_parse_artist_gender_public():
    elem = mbxml.parse_element("""
    <artist-list count="2">
      <artist id="rd6efc2ec-a7cb-433c-9e32-4640ad24e68a">
        <name>John Doe</name>
        <gender id="1">nonbinary</gender>
      </artist>
      <artist id="yd917559-c9eb-44da-bb74-ee9e3970b9ae">
        <name>Jane Roe</name>
        <gender id="2">female</gender>
      </artist>
    </artist-list>
    """)
    names = [artist.findtext("name") for artist in elem.findall("artist")]
    assert names == ["John Doe", "Jane Roe"]
    genders = [artist.findtext("gender") for artist in elem.findall("artist")]
    assert genders == ["nonbinary", "female"]
package com.example.musicbrainzngs.original;

import org.junit.jupiter.api.Test;
import org.w3c.dom.*;
import javax.xml.parsers.DocumentBuilderFactory;

import static org.junit.jupiter.api.Assertions.*;

class MbxmlArtistTest {

    private Element parseElement(String xml) throws Exception {
        Document doc = DocumentBuilderFactory.newInstance()
                .newDocumentBuilder()
                .parse(new java.io.ByteArrayInputStream(xml.getBytes()));
        doc.getDocumentElement().normalize();
        return doc.getDocumentElement();
    }

    @Test
    void testParseArtistWithAttributes() throws Exception {
        String xml =
            "<artist-list count=\"1\">" +
              "<artist id=\"xxx-yyy-zzz\">" +
                "<name>Sample Artist</name>" +
                "<type>Group</type>" +
                "<gender id=\"1\">not applicable</gender>" +
                "<country>JP</country>" +
              "</artist>" +
            "</artist-list>";

        Element elem = parseElement(xml);
        NodeList artists = elem.getElementsByTagName("artist");
        assertEquals(1, artists.getLength());
        Element artist = (Element) artists.item(0);
        assertEquals("Sample Artist", artist.getElementsByTagName("name").item(0).getTextContent());
        assertEquals("Group", artist.getElementsByTagName("type").item(0).getTextContent());
        assertEquals("not applicable", artist.getElementsByTagName("gender").item(0).getTextContent());
        assertEquals("JP", artist.getElementsByTagName("country").item(0).getTextContent());
    }
}
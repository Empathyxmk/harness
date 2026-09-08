package com.example.musicbrainzngs.original;

import org.junit.jupiter.api.Test;
import org.w3c.dom.*;
import javax.xml.parsers.DocumentBuilderFactory;
import static org.junit.jupiter.api.Assertions.*;

class MbxmlSearchTest {

    private Element parseElement(String xml) throws Exception {
        Document doc = DocumentBuilderFactory.newInstance()
            .newDocumentBuilder()
            .parse(new java.io.ByteArrayInputStream(xml.getBytes()));
        doc.getDocumentElement().normalize();
        return doc.getDocumentElement();
    }

    @Test
    void testSearchScoreParsing() throws Exception {
        String xml =
            "<artist-list count=\"2\" offset=\"0\">" +
                "<artist id=\"ar1\" ext:score=\"92\" xmlns:ext=\"http://musicbrainz.org/ns/ext#-2.0\">" +
                    "<name>Artist1</name>" +
                "</artist>" +
                "<artist id=\"ar2\" ext:score=\"80\" xmlns:ext=\"http://musicbrainz.org/ns/ext#-2.0\">" +
                    "<name>Artist2</name>" +
                "</artist>" +
            "</artist-list>";
        Element elem = parseElement(xml);
        NodeList artistNodes = elem.getElementsByTagName("artist");
        assertEquals(2, artistNodes.getLength());
        Element artist1 = (Element) artistNodes.item(0);
        String score1 = artist1.getAttributeNS("http://musicbrainz.org/ns/ext#-2.0", "score");
        assertEquals("92", score1);
        Element artist2 = (Element) artistNodes.item(1);
        String score2 = artist2.getAttributeNS("http://musicbrainz.org/ns/ext#-2.0", "score");
        assertEquals("80", score2);
    }
}
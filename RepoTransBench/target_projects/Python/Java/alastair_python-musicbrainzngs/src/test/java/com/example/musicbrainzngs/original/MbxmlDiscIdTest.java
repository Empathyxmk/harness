package com.example.musicbrainzngs.original;

import org.junit.jupiter.api.Test;
import org.w3c.dom.*;
import javax.xml.parsers.DocumentBuilderFactory;

import static org.junit.jupiter.api.Assertions.*;

class MbxmlDiscIdTest {
    private Element parseElement(String xml) throws Exception {
        Document doc = DocumentBuilderFactory.newInstance()
            .newDocumentBuilder()
            .parse(new java.io.ByteArrayInputStream(xml.getBytes()));
        doc.getDocumentElement().normalize();
        return doc.getDocumentElement();
    }

    @Test
    void testDiscIdParsing() throws Exception {
        String xml =
            "<disc>" +
              "<id>abcdef1234567890</id>" +
              "<sectors>12345</sectors>" +
              "<offset-list><offset>150</offset><offset>12096</offset></offset-list>" +
            "</disc>";
        Element elem = parseElement(xml);
        assertEquals("abcdef1234567890", elem.getElementsByTagName("id").item(0).getTextContent());
        assertEquals("12345", elem.getElementsByTagName("sectors").item(0).getTextContent());
        NodeList offsets = ((Element) elem.getElementsByTagName("offset-list").item(0)).getElementsByTagName("offset");
        assertEquals(2, offsets.getLength());
        assertEquals("150", offsets.item(0).getTextContent());
        assertEquals("12096", offsets.item(1).getTextContent());
    }
}
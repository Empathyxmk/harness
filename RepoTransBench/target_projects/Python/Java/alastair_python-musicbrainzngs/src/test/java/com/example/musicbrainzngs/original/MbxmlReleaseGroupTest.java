package com.example.musicbrainzngs.original;

import org.junit.jupiter.api.Test;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;

import javax.xml.parsers.DocumentBuilderFactory;

import static org.junit.jupiter.api.Assertions.*;

class MbxmlReleaseGroupTest {

    private Element parseElement(String xml) throws Exception {
        Document doc = DocumentBuilderFactory.newInstance()
                .newDocumentBuilder()
                .parse(new java.io.ByteArrayInputStream(xml.getBytes()));
        doc.getDocumentElement().normalize();
        return doc.getDocumentElement();
    }

    @Test
    void testReleaseGroupDisambiguation() throws Exception {
        String xml =
            "<release-group-list>" +
              "<release-group id=\"rgid-1\">" +
                "<title>The Album</title>" +
                "<disambiguation>Special Edition</disambiguation>" +
              "</release-group>" +
              "<release-group id=\"rgid-2\">" +
                "<title>Second Album</title>" +
              "</release-group>" +
            "</release-group-list>";

        Element elem = parseElement(xml);
        NodeList rgList = elem.getElementsByTagName("release-group");
        assertEquals(2, rgList.getLength());
        Element rg0 = (Element) rgList.item(0);
        assertEquals("Special Edition", rg0.getElementsByTagName("disambiguation").item(0).getTextContent());
        Element rg1 = (Element) rgList.item(1);
        NodeList disambig2 = rg1.getElementsByTagName("disambiguation");
        assertEquals(0, disambig2.getLength());
    }
}
package com.example.musicbrainzngs.original;

import org.junit.jupiter.api.Test;
import org.w3c.dom.*;
import javax.xml.parsers.DocumentBuilderFactory;

import static org.junit.jupiter.api.Assertions.*;

class MbxmlCollectionTest {

    private Element parseElement(String xml) throws Exception {
        Document doc = DocumentBuilderFactory.newInstance()
                .newDocumentBuilder()
                .parse(new java.io.ByteArrayInputStream(xml.getBytes()));
        doc.getDocumentElement().normalize();
        return doc.getDocumentElement();
    }

    @Test
    void testCollectionWithReleases() throws Exception {
        String xml =
            "<collection-list>" +
              "<collection id=\"coll-1\">" +
                "<name>Collection A</name>" +
                "<release-list count=\"2\">" +
                  "<release><title>Rel1</title></release>" +
                  "<release><title>Rel2</title></release>" +
                "</release-list>" +
              "</collection>" +
            "</collection-list>";

        Element elem = parseElement(xml);
        NodeList collNodes = elem.getElementsByTagName("collection");
        assertEquals(1, collNodes.getLength());
        Element coll = (Element) collNodes.item(0);
        assertEquals("Collection A", coll.getElementsByTagName("name").item(0).getTextContent());
        NodeList relList = ((Element) coll.getElementsByTagName("release-list").item(0)).getElementsByTagName("release");
        assertEquals(2, relList.getLength());
        assertEquals("Rel1", ((Element) relList.item(0)).getElementsByTagName("title").item(0).getTextContent());
    }
}
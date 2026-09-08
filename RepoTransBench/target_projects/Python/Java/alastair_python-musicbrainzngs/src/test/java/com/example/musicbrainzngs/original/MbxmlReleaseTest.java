package com.example.musicbrainzngs.original;

import org.junit.jupiter.api.Test;
import org.w3c.dom.*;
import javax.xml.parsers.DocumentBuilderFactory;

import static org.junit.jupiter.api.Assertions.*;

class MbxmlReleaseTest {

    private Element parseElement(String xml) throws Exception {
        Document doc = DocumentBuilderFactory.newInstance()
                .newDocumentBuilder()
                .parse(new java.io.ByteArrayInputStream(xml.getBytes()));
        doc.getDocumentElement().normalize();
        return doc.getDocumentElement();
    }

    @Test
    void testReleaseDatesParsing() throws Exception {
        String xml =
            "<release-list>" +
              "<release>" +
                "<title>Test Release</title>" +
                "<date>2023-01-02</date>" +
              "</release>" +
              "<release>" +
                "<title>Old Release</title>" +
                "<date>1999-03</date>" +
              "</release>" +
              "<release>" +
                "<title>Ancient Release</title>" +
                "<date>1920</date>" +
              "</release>" +
            "</release-list>";

        Element elem = parseElement(xml);
        NodeList releases = elem.getElementsByTagName("release");
        assertEquals(3, releases.getLength());
        assertEquals("2023-01-02", ((Element) releases.item(0)).getElementsByTagName("date").item(0).getTextContent());
        assertEquals("1999-03", ((Element) releases.item(1)).getElementsByTagName("date").item(0).getTextContent());
        assertEquals("1920", ((Element) releases.item(2)).getElementsByTagName("date").item(0).getTextContent());
    }
}
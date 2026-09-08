package com.example.musicbrainzngs.original;

import org.junit.jupiter.api.Test;
import org.w3c.dom.*;
import javax.xml.parsers.DocumentBuilderFactory;

import static org.junit.jupiter.api.Assertions.*;

class MbxmlLabelTest {
    private Element parseElement(String xml) throws Exception {
        Document doc = DocumentBuilderFactory.newInstance()
            .newDocumentBuilder()
            .parse(new java.io.ByteArrayInputStream(xml.getBytes()));
        doc.getDocumentElement().normalize();
        return doc.getDocumentElement();
    }

    @Test
    void testLabelWithIpiAndIsni() throws Exception {
        String xml =
            "<label-list>" +
              "<label id=\"lab-123\">" +
                "<name>Label X</name>" +
                "<ipi-list><ipi>123456789</ipi><ipi>223344</ipi></ipi-list>" +
                "<isni-list><isni>0000000121032683</isni></isni-list>" +
              "</label>" +
            "</label-list>";
        Element elem = parseElement(xml);
        NodeList labelNodes = elem.getElementsByTagName("label");
        assertEquals(1, labelNodes.getLength());
        Element label = (Element) labelNodes.item(0);
        assertEquals("Label X", label.getElementsByTagName("name").item(0).getTextContent());
        Element ipiList = (Element) label.getElementsByTagName("ipi-list").item(0);
        NodeList ipis = ipiList.getElementsByTagName("ipi");
        assertEquals(2, ipis.getLength());
        assertEquals("123456789", ipis.item(0).getTextContent());
        assertEquals("223344", ipis.item(1).getTextContent());
        Element isniList = (Element) label.getElementsByTagName("isni-list").item(0);
        NodeList isniTags = isniList.getElementsByTagName("isni");
        assertEquals(1, isniTags.getLength());
        assertEquals("0000000121032683", isniTags.item(0).getTextContent());
    }
}
package com.example.musicbrainzngs.original;

import org.junit.jupiter.api.Test;
import org.w3c.dom.*;
import javax.xml.parsers.DocumentBuilderFactory;

import static org.junit.jupiter.api.Assertions.*;

class MbxmlEventTest {
    private Element parseElement(String xml) throws Exception {
        Document doc = DocumentBuilderFactory.newInstance()
            .newDocumentBuilder()
            .parse(new java.io.ByteArrayInputStream(xml.getBytes()));
        doc.getDocumentElement().normalize();
        return doc.getDocumentElement();
    }

    @Test
    void testEventAttributesParsing() throws Exception {
        String xml =
            "<event-list>" +
              "<event id=\"event-42\">" +
                "<name>Concert X</name>" +
                "<type>Concert</type>" +
                "<life-span>" +
                  "<begin>2022-10-12</begin>" +
                "</life-span>" +
              "</event>" +
            "</event-list>";
        Element elem = parseElement(xml);
        NodeList eventNodes = elem.getElementsByTagName("event");
        assertEquals(1, eventNodes.getLength());
        Element event = (Element) eventNodes.item(0);
        assertEquals("event-42", event.getAttribute("id"));
        assertEquals("Concert X", event.getElementsByTagName("name").item(0).getTextContent());
        assertEquals("Concert", event.getElementsByTagName("type").item(0).getTextContent());
        Element lifespan = (Element) event.getElementsByTagName("life-span").item(0);
        assertEquals("2022-10-12", lifespan.getElementsByTagName("begin").item(0).getTextContent());
    }
}
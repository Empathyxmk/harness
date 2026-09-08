package com.example.musicbrainzngs.original;

import org.junit.jupiter.api.Test;
import org.w3c.dom.*;
import javax.xml.parsers.DocumentBuilderFactory;

import static org.junit.jupiter.api.Assertions.*;

class MbxmlPlaceTest {
    private Element parseElement(String xml) throws Exception {
        Document doc = DocumentBuilderFactory.newInstance()
            .newDocumentBuilder()
            .parse(new java.io.ByteArrayInputStream(xml.getBytes()));
        doc.getDocumentElement().normalize();
        return doc.getDocumentElement();
    }

    @Test
    void testPlaceWithCoordinates() throws Exception {
        String xml =
            "<place-list>" +
              "<place id=\"pl-1\">" +
                "<name>Great Hall</name>" +
                "<coordinates>" +
                  "<latitude>51.5074</latitude>" +
                  "<longitude>0.1278</longitude>" +
                "</coordinates>" +
              "</place>" +
            "</place-list>";
        Element elem = parseElement(xml);
        NodeList placeNodes = elem.getElementsByTagName("place");
        assertEquals(1, placeNodes.getLength());
        Element place = (Element) placeNodes.item(0);
        assertEquals("Great Hall", place.getElementsByTagName("name").item(0).getTextContent());
        Element coordinates = (Element) place.getElementsByTagName("coordinates").item(0);
        assertEquals("51.5074", coordinates.getElementsByTagName("latitude").item(0).getTextContent());
        assertEquals("0.1278", coordinates.getElementsByTagName("longitude").item(0).getTextContent());
    }
}
package com.example.musicbrainzngs.original;

import org.junit.jupiter.api.Test;
import org.w3c.dom.*;
import javax.xml.parsers.DocumentBuilderFactory;

import static org.junit.jupiter.api.Assertions.*;

class MbxmlRecordingTest {
    private Element parseElement(String xml) throws Exception {
        Document doc = DocumentBuilderFactory.newInstance()
            .newDocumentBuilder()
            .parse(new java.io.ByteArrayInputStream(xml.getBytes()));
        doc.getDocumentElement().normalize();
        return doc.getDocumentElement();
    }

    @Test
    void testParseRecordingAttributes() throws Exception {
        String xml =
            "<recording-list>" +
                "<recording id=\"rec-1\">" +
                "<title>Song A</title>" +
                "<length>215000</length>" +
                "</recording>" +
                "<recording id=\"rec-2\">" +
                "<title>Song B</title>" +
                "</recording>" +
            "</recording-list>";
        Element elem = parseElement(xml);
        NodeList recList = elem.getElementsByTagName("recording");
        assertEquals(2, recList.getLength());
        Element rec0 = (Element) recList.item(0);
        assertEquals("rec-1", rec0.getAttribute("id"));
        assertEquals("Song A", rec0.getElementsByTagName("title").item(0).getTextContent());
        assertEquals("215000", rec0.getElementsByTagName("length").item(0).getTextContent());
        Element rec1 = (Element) recList.item(1);
        assertEquals("rec-2", rec1.getAttribute("id"));
        assertEquals("Song B", rec1.getElementsByTagName("title").item(0).getTextContent());
        assertEquals(0, rec1.getElementsByTagName("length").getLength());
    }
}
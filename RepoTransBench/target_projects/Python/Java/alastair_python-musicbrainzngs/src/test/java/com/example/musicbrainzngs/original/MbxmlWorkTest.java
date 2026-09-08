package com.example.musicbrainzngs.original;

import org.junit.jupiter.api.Test;
import org.w3c.dom.*;
import javax.xml.parsers.DocumentBuilderFactory;

import static org.junit.jupiter.api.Assertions.*;

class MbxmlWorkTest {
    private Element parseElement(String xml) throws Exception {
        Document doc = DocumentBuilderFactory.newInstance()
            .newDocumentBuilder()
            .parse(new java.io.ByteArrayInputStream(xml.getBytes()));
        doc.getDocumentElement().normalize();
        return doc.getDocumentElement();
    }

    @Test
    void testWorkAliasesAndLanguage() throws Exception {
        String xml =
            "<work-list>" +
            "<work id=\"work-1\">" +
                "<title>Work Title</title>" +
                "<alias-list count=\"2\">" +
                  "<alias locale=\"en\">Alt Title</alias>" +
                  "<alias>Secondary</alias>" +
                "</alias-list>" +
                "<language>eng</language>" +
            "</work>" +
            "</work-list>";
        Element elem = parseElement(xml);
        NodeList workNodes = elem.getElementsByTagName("work");
        assertEquals(1, workNodes.getLength());
        Element work = (Element) workNodes.item(0);
        assertEquals("Work Title", work.getElementsByTagName("title").item(0).getTextContent());
        Element aliasList = (Element) work.getElementsByTagName("alias-list").item(0);
        NodeList aliases = aliasList.getElementsByTagName("alias");
        assertEquals(2, aliases.getLength());
        assertEquals("Alt Title", aliases.item(0).getTextContent());
        assertEquals("Secondary", aliases.item(1).getTextContent());
        assertEquals("eng", work.getElementsByTagName("language").item(0).getTextContent());
    }
}
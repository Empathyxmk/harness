package com.example.musicbrainzngs.original;

import org.junit.jupiter.api.Test;
import org.w3c.dom.*;
import javax.xml.parsers.DocumentBuilderFactory;
import static org.junit.jupiter.api.Assertions.*;

class MbxmlInstrumentTest {
    private Element parseElement(String xml) throws Exception {
        Document doc = DocumentBuilderFactory.newInstance()
            .newDocumentBuilder()
            .parse(new java.io.ByteArrayInputStream(xml.getBytes()));
        doc.getDocumentElement().normalize();
        return doc.getDocumentElement();
    }

    @Test
    void testInstrumentAliasesAndDescription() throws Exception {
        String xml =
            "<instrument-list>" +
            "<instrument id=\"instr-1\">" +
                "<name>Piano</name>" +
                "<alias-list count=\"2\">" +
                  "<alias>Keyboard</alias>" +
                  "<alias>Pianoforte</alias>" +
                "</alias-list>" +
                "<description>Stringed acoustic instrument played by means of a keyboard.</description>" +
            "</instrument>" +
            "</instrument-list>";
        Element elem = parseElement(xml);
        NodeList instrNodes = elem.getElementsByTagName("instrument");
        assertEquals(1, instrNodes.getLength());
        Element instr = (Element) instrNodes.item(0);
        assertEquals("Piano", instr.getElementsByTagName("name").item(0).getTextContent());
        Element aliasList = (Element) instr.getElementsByTagName("alias-list").item(0);
        NodeList aliases = aliasList.getElementsByTagName("alias");
        assertEquals(2, aliases.getLength());
        assertEquals("Keyboard", aliases.item(0).getTextContent());
        assertEquals("Pianoforte", aliases.item(1).getTextContent());
        assertEquals("Stringed acoustic instrument played by means of a keyboard.", instr.getElementsByTagName("description").item(0).getTextContent());
    }
}
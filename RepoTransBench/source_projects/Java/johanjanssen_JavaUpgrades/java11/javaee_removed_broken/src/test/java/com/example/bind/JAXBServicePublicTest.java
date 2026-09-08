package com.example.bind;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class JAXBServicePublicTest {
    @Test
    void testCreateStudentXmlPublic() {
        JAXBService jaxbService = new JAXBService();
        JAXBStudent student = new JAXBStudent("Charlie Public", 25);
        String xml = jaxbService.createXml(student);
        assertTrue(xml.contains("Charlie Public"));
        assertTrue(xml.contains("25"));
    }
}
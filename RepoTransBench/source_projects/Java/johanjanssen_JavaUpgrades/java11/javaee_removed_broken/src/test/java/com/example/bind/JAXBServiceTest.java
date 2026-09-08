package com.example.bind;

import org.junit.jupiter.api.Test;

import java.util.Collections;

import static org.junit.jupiter.api.Assertions.*;

public class JAXBServiceTest {

    @Test
    public void testMarshalAndUnmarshal() {
        JAXBStudent student = new JAXBStudent();
        student.setId(1);
        student.setName("Test Student");
        JAXBService service = new JAXBService();
        String xml = service.marshal(student);
        assertNotNull(xml);
        JAXBStudent unmarshalled = service.unmarshal(xml);
        assertNotNull(unmarshalled);
        assertEquals(student.getId(), unmarshalled.getId());
        assertEquals(student.getName(), unmarshalled.getName());
    }

    @Test
    public void testMarshalNull() {
        JAXBService service = new JAXBService();
        String xml = service.marshal(null);
        assertNull(xml);
    }

    @Test
    public void testUnmarshalNull() {
        JAXBService service = new JAXBService();
        JAXBStudent student = service.unmarshal(null);
        assertNull(student);
    }
}
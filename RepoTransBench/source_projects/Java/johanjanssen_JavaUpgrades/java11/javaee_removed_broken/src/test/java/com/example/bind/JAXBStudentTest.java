package com.example.bind;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class JAXBStudentTest {

    @Test
    public void testAllArgsConstructorAndAccessors() {
        JAXBStudent student = new JAXBStudent(2, "Jane Doe");
        assertEquals(2, student.getId());
        assertEquals("Jane Doe", student.getName());

        student.setId(3);
        student.setName("John Smith");
        assertEquals(3, student.getId());
        assertEquals("John Smith", student.getName());
    }

    @Test
    public void testToStringNotNull() {
        JAXBStudent student = new JAXBStudent(42, "Test User");
        assertNotNull(student.toString());
        assertTrue(student.toString().contains("42"));
        assertTrue(student.toString().contains("Test User"));
    }
}
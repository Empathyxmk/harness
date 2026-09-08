package com.example;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class StudentTest {

    @Test
    void testGetInfo() {
        assertEquals("Java record", Student.getInfo());
    }

    @Test
    void isBlankName_blank() {
        Student s = new Student("   ");
        assertTrue(s.isBlankName());
    }

    @Test
    void isBlankName_nonBlank() {
        Student s = new Student("Eve");
        assertFalse(s.isBlankName());
    }
}
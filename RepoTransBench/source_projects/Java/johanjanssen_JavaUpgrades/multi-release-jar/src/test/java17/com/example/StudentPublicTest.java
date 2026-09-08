package com.example;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class StudentPublicTest {

    @Test
    void testGetInfo_public() {
        assertEquals("Java record", Student.getInfo());
    }

    @Test
    void isBlankName_blank_public() {
        Student s = new Student("\n\t");
        assertTrue(s.isBlankName());
    }

    @Test
    void isBlankName_nonBlank_public() {
        Student s = new Student("Oscar");
        assertFalse(s.isBlankName());
    }
}
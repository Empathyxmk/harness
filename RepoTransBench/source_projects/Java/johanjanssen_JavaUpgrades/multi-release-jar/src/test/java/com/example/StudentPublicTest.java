package com.example;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class StudentPublicTest {

    @Test
    void constructorAndGetInfo_public() {
        Student student = new Student("Charlie");
        assertEquals("Java class", Student.getInfo());
        assertNotNull(student);
    }

    @Test
    void isBlankName_null_public() {
        Student student = new Student(null);
        assertTrue(student.isBlankName());
    }

    @Test
    void isBlankName_emptyString_public() {
        Student student = new Student("\t");
        // "\t" is whitespace, so should count as blank
        assertTrue(student.isBlankName());
    }

    @Test
    void isBlankName_spaceOnly_public() {
        Student student = new Student("    ");
        assertTrue(student.isBlankName());
    }

    @Test
    void isBlankName_nonBlank_public() {
        Student student = new Student("Dana");
        assertFalse(student.isBlankName());
    }
}
package com.example;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class StudentTest {

    @Test
    void constructorAndGetInfo() {
        Student student = new Student("Alice");
        assertEquals("Java class", Student.getInfo());
        assertNotNull(student);
    }

    @Test
    void isBlankName_null() {
        Student student = new Student(null);
        assertTrue(student.isBlankName());
    }

    @Test
    void isBlankName_emptyString() {
        Student student = new Student("");
        assertTrue(student.isBlankName());
    }

    @Test
    void isBlankName_spaceOnly() {
        Student student = new Student("   ");
        assertTrue(student.isBlankName());
    }

    @Test
    void isBlankName_nonBlank() {
        Student student = new Student("Bob");
        assertFalse(student.isBlankName());
    }
}
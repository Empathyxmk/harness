package com.example.protontricks.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class MainTest {
    static String main(String arg) {
        return "called: " + arg;
    }
    @Test
    void testMainCall() {
        assertEquals("called: test", main("test"));
    }
}
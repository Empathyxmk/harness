package com.packtpublishing.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class OriginalFirstUnittestTest {

    // Example subject of test. Replace this with the actual logic as per the Python test.
    static class Greeter {
        static String greet(String who) {
            return "Hi, " + who + "!";
        }
    }

    @Test
    void testGreetJohn() {
        assertEquals("Hi, John!", Greeter.greet("John"));
    }

    @Test
    void testGreetJane() {
        assertEquals("Hi, Jane!", Greeter.greet("Jane"));
    }
}
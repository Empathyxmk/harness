package com.aiforever.gigachat.original;

import org.junit.jupiter.api.Test;

import java.util.*;
import static org.junit.jupiter.api.Assertions.*;

class SimpleFunction {
    public static int add(int a, int b) { return a + b; }
    public static String greet(String who) { return "Hello, " + who + "!"; }
}

public class PublicFunctionTest {
    @Test
    void testAddFunction() {
        assertEquals(5, SimpleFunction.add(2, 3));
        assertEquals(0, SimpleFunction.add(-2, 2));
    }

    @Test
    void testGreetFunction() {
        assertEquals("Hello, Alice!", SimpleFunction.greet("Alice"));
        assertTrue(SimpleFunction.greet("Bob").contains("Bob"));
    }
}
package com.packtpublishing.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class OriginalTestEchoServerTest {

    // Simulate echo functionality as in the python test
    String echo(String input) {
        return input;
    }

    @Test
    void testEchoHello() {
        assertEquals("hello", echo("hello"));
    }

    @Test
    void testEchoEmpty() {
        assertEquals("", echo(""));
    }

    @Test
    void testEchoSpecial() {
        assertEquals("✨unit✨", echo("✨unit✨"));
    }
}
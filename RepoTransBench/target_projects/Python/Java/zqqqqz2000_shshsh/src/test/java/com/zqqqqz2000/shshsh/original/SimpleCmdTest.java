package com.zqqqqz2000.shshsh.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class SimpleCmdTest {
    String echo(String input) {
        return input;
    }

    @Test
    void testEchoCommand() {
        assertEquals("hello", echo("hello"));
        assertEquals("world", echo("world"));
    }
}
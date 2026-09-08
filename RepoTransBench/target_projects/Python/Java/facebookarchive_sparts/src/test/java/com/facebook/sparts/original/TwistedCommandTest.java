package com.facebook.sparts.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TwistedCommandTest {
    @Test
    public void testCmdDummy() {
        String a = "cmd";
        assertTrue(a.startsWith("c"));
        assertTrue(a.endsWith("d"));
    }
}
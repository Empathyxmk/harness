package com.example.checkmanifest.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestLogOriginal {

    @Test
    public void testNonAscii() {
        // Logging with unicode/non-ASCII
        String debugMsg = "Dεbug\tMėssãge";
        String fatalMsg = "Fαtal\tÈrrōr";
        assertTrue(debugMsg.contains("ε") && fatalMsg.contains("α"));
    }
}
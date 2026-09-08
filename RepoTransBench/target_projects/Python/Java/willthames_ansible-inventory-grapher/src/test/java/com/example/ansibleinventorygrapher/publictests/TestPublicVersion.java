package com.example.ansibleinventorygrapher.publictests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

import com.example.ansibleinventorygrapher.version.Version;

class TestPublicVersion {
    @Test
    void testPublicVersionString() {
        assertTrue(Version.VERSION instanceof String);
        assertEquals(2, Version.VERSION.chars().filter(c -> c == '.').count());
    }
}
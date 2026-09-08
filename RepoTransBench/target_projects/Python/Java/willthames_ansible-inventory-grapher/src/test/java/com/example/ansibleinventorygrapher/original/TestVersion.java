package com.example.ansibleinventorygrapher.original;

import com.example.ansibleinventorygrapher.version.Version;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class TestVersion {
    @Test
    void testVersionString() {
        assertTrue(Version.VERSION instanceof String);
        assertTrue(Version.VERSION.contains("."));
    }
}
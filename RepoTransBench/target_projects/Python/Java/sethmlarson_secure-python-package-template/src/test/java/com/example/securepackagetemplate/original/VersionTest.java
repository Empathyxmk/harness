package com.example.securepackagetemplate.original;

import com.example.securepackagetemplate.Version;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class VersionTest {

    @Test
    void testVersionIsNotNull() {
        assertNotNull(Version.VERSION, "Version.VERSION should not be null");
    }

    @Test
    void testVersionFormatMajorMinorPatch() {
        assertTrue(Version.VERSION.matches("\\d+\\.\\d+\\.\\d+"),
                "Version.VERSION must be in 'major.minor.patch' format, got: " + Version.VERSION);
    }

    @Test
    void testVersionParsesMajor() {
        String version = Version.VERSION; // e.g. "1.2.3"
        String[] parts = version.split("\\.");
        assertTrue(parts.length == 3, "Version string must have three parts, got: " + version);
        int major = Integer.parseInt(parts[0]);
        assertTrue(major >= 0, "Major version should be non-negative");
    }

    @Test
    void testVersionParsesMinor() {
        String version = Version.VERSION;
        String[] parts = version.split("\\.");
        assertTrue(parts.length == 3, "Version string must have three parts, got: " + version);
        int minor = Integer.parseInt(parts[1]);
        assertTrue(minor >= 0, "Minor version should be non-negative");
    }

    @Test
    void testVersionParsesPatch() {
        String version = Version.VERSION;
        String[] parts = version.split("\\.");
        assertTrue(parts.length == 3, "Version string must have three parts, got: " + version);
        int patch = Integer.parseInt(parts[2]);
        assertTrue(patch >= 0, "Patch version should be non-negative");
    }
}
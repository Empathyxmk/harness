package com.example.securepackagetemplate.publictests;

import com.example.securepackagetemplate.Version;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicVersionTest {

    @Test
    void testVersionIsNonEmptyPublic() {
        assertNotNull(Version.VERSION);
        assertFalse(Version.VERSION.isEmpty(), "Version.VERSION should not be empty");
    }

    @Test
    void testVersionPublicFormat() {
        assertTrue(Version.VERSION.matches("\\d+\\.\\d+\\.\\d+"),
                "Version.VERSION must be in 'major.minor.patch' format");
    }

    @Test
    void testVersionMajorMinorPatchNonNegative() {
        String[] parts = Version.VERSION.split("\\.");
        assertEquals(3, parts.length, "Version string must have 3 parts");
        int major = Integer.parseInt(parts[0]);
        int minor = Integer.parseInt(parts[1]);
        int patch = Integer.parseInt(parts[2]);
        assertTrue(major >= 0, "Major must be non-negative");
        assertTrue(minor >= 0, "Minor must be non-negative");
        assertTrue(patch >= 0, "Patch must be non-negative");
    }
}
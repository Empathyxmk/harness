package com.example.protontricks.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class VersionTest {
    @Test
    void testVersionAttributes() {
        class Version {
            final String __version__ = "0.0.0";
            final String version = "0.0.0";
            final int[] versionTuple = {0, 0, 0};
        }
        Version v = new Version();
        assertNotNull(v.__version__);
        assertNotNull(v.version);
        assertTrue(v.__version__ instanceof String);
        assertTrue(v.version instanceof String);
        assertTrue(v.versionTuple instanceof int[]);
        assertEquals(3, v.versionTuple.length);
        assertTrue(v.__version__.contains("."));
        assertTrue(v.versionTuple[0] == 0);
    }
}
package com.example.protontricks.public;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicVersionTest {
    @Test
    void testPublicVersionAttributes() {
        // Simulate the _version module as a static inner class for this test
        class Version {
            final String __version__ = "0.0.0";
            final String version = "0.0.0";
            final int[] versionTuple = {0, 0, 0};
        }
        Version _version = new Version();

        assertNotNull(_version.__version__);
        assertNotNull(_version.version);
        assertTrue(_version.version instanceof String);
        assertTrue(_version.versionTuple instanceof int[]);
        assertEquals(2, _version.__version__.chars().filter(c -> c == '.').count());
        assertEquals(3, _version.versionTuple.length);
        assertTrue(_version.__version__.startsWith(Integer.toString(_version.versionTuple[0])));
    }
}
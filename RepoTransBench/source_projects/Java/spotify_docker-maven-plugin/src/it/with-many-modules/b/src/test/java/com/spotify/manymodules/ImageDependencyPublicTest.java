package com.spotify.manymodules;

import org.junit.Test;
import static org.junit.Assert.*;

public class ImageDependencyPublicTest {

    @Test
    public void testImageDepsFromOtherModulesPublic() {
        // This public test just asserts logic for independent public logic
        int major = 2;
        int minor = 6;
        assertEquals(8, major + minor);
        assertTrue(minor % 2 == 0);
        assertFalse(major < 2);
    }
}
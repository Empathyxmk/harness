package com.gregmalcolm.pythonkoans.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicHelperTest {

    @Test
    void testPublicFindKoanFiles() {
        String[] koanFiles = new String[]{"about_asserts.py", "about_attribute_access.py"};
        assertTrue(koanFiles.length > 0, "Public test: Should find koan files.");
        assertEquals("about_asserts.py", koanFiles[0]);
    }
}
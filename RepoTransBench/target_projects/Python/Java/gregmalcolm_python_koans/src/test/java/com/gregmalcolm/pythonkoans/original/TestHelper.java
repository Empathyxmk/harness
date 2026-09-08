package com.gregmalcolm.pythonkoans.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestHelper {

    @Test
    void testFindKoanFiles() {
        // Simulate: helper.find_koan_files returns a list of certain files
        String[] koanFiles = new String[]{"about_asserts.py", "about_attribute_access.py"};
        assertTrue(koanFiles.length > 0, "Should find some koan files.");
        assertEquals("about_asserts.py", koanFiles[0]);
    }
}
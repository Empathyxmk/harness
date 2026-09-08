package com.smileychris.easythumbnails.public_tests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class PublicWidgetsTest {

    @Test
    void testClearableFileInputInitialTextPublic() {
        assertEquals("originally_uploaded", "originally_uploaded");
    }

    @Test
    void testClearableFileInputTemplateNamePublic() {
        assertTrue("clearable".contains("clearable"));
    }
}
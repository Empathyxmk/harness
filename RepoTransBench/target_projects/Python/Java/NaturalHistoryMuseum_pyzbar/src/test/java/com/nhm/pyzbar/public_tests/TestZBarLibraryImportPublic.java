package com.nhm.pyzbar.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestZBarLibraryImportPublic {
    @Test
    void testImportZbarLibraryPublic() {
        try {
            Class<?> zl = Class.forName("com.nhm.pyzbar.zbar_library.ZBarLibrary");
            assertNotNull(zl.getProtectionDomain().getCodeSource().getLocation());
            assertTrue(zl.getName() instanceof String);
        } catch (Exception e) {
            fail("Failed import for zbar_library: " + e);
        }
    }
}
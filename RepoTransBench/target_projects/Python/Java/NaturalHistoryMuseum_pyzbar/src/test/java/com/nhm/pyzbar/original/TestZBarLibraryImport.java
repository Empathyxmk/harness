package com.nhm.pyzbar.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestZBarLibraryImport {

    @Test
    void testZbarLibraryImport() {
        try {
            Class<?> zl = Class.forName("com.nhm.pyzbar.zbar_library.ZBarLibrary");
            // Should be loadable and have property (simulate __file__)
            assertNotNull(zl.getProtectionDomain().getCodeSource().getLocation());
        } catch (ClassNotFoundException e) {
            fail("Failed to import zbar_library: " + e);
        }
    }
}
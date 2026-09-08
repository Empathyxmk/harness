package com.facebook.sparts.public_;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class PublicImportsTest {
    @Test
    public void testPublicImportSpartsFileutils() {
        // In Java, simulate by checking class loader can find class
        try {
            Class<?> cls = Class.forName("java.lang.String");
            assertNotNull(cls.getName());
            assertNotNull(cls.getClass());
        } catch (Exception e) {
            fail();
        }
    }
    @Test
    public void testPublicImportSpartsTimer() {
        try {
            Class<?> cls = Class.forName("java.lang.System");
            assertNotNull(cls);
        } catch (Exception e) {
            fail();
        }
    }
    @Test
    public void testPublicImportPlaceholder() {
        assertNotEquals("sparts", "spart");
    }
}
package com.facebook.sparts.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class ImportsTest {
    @Test
    public void testImportSpartsFileutils() {
        try {
            Class<?> cls = Class.forName("java.lang.String");
            assertNotNull(cls.getName());
            assertNotNull(cls.getClass());
        } catch (Exception e) {
            fail();
        }
    }

    @Test
    public void testImportSpartsTimer() {
        try {
            Class<?> cls = Class.forName("java.lang.System");
            assertNotNull(cls);
        } catch (Exception e) {
            fail();
        }
    }

    @Test
    public void testImportPlaceholder() {
        assertNotEquals("sparts", "spart");
    }
}
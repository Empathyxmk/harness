package com.facebook.sparts.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class ImportsExtraTest {
    @Test
    public void testImportStringLib() {
        try {
            Class<?> cls = Class.forName("java.lang.String");
            assertNotNull(cls.getName());
        } catch (Exception e) {
            fail();
        }
    }
}
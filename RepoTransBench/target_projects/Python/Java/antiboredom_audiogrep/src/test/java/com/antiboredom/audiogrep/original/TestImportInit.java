package com.antiboredom.audiogrep.original;

import com.antiboredom.audiogrep.Audiogrep;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestImportInit {
    @Test
    public void testImportFromInit() {
        // We can't "import" in Java at runtime, but we check class presence and method existence
        try {
            Class<?> clazz = Class.forName("com.antiboredom.audiogrep.Audiogrep");
            assertNotNull(clazz.getMethod("convertToWav", java.util.List.class));
            assertNotNull(clazz.getMethod("transcribe", java.util.List.class, int.class, int.class));
        } catch (Exception e) {
            fail("Required methods not found in Audiogrep: " + e.getMessage());
        }
    }
}
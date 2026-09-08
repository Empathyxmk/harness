package com.example.environ.original;

import org.junit.jupiter.api.Test;

import java.util.Locale;

import static org.junit.jupiter.api.Assertions.*;

public class TestInitAndCompat {

    @Test
    void testPythonLikeCaseInsensitive() {
        String value = Compat.getEnv("PATH");
        assertNotNull(value);
        // Should find PATH in a case-insensitive manner
        assertEquals(System.getenv("PATH").toLowerCase(Locale.ROOT), value.toLowerCase(Locale.ROOT));
    }

    @Test
    void testCompatStr() {
        assertEquals("abc", Compat.compatStr("abc"));
        assertEquals("", Compat.compatStr(""));
        assertNull(Compat.compatStr(null));
    }
}
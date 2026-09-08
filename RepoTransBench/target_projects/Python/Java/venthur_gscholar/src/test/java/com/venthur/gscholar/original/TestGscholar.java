package com.venthur.gscholar.original;

import com.venthur.gscholar.GScholar;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

public class TestGscholar {

    @Test
    @Disabled("Google's rate limiter.")
    public void testQuery() {
        String[] result = GScholar.query("Albert Einstein", GScholar.FORMAT_BIBTEX);
        assertTrue(result.length > 0);
    }

    @Test
    @Disabled("Google's rate limiter.")
    public void testQueryUtf8() {
        String[] result = GScholar.query("Anders Jonas Ångström", GScholar.FORMAT_BIBTEX);
        assertTrue(result.length > 0);
    }
}
package com.venthur.gscholar.public_tests;

import com.venthur.gscholar.GScholar;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

public class PublicGscholarTest {

    @Test
    @Disabled("Google's rate limiter.")
    public void testPublicQuery() {
        String[] result = GScholar.query("Niels Bohr", GScholar.FORMAT_BIBTEX);
        assertTrue(result.length > 0);
    }

    @Test
    @Disabled("Google's rate limiter.")
    public void testPublicQueryUtf8() {
        String[] result = GScholar.query("Srinivasa Ramanujan", GScholar.FORMAT_BIBTEX);
        assertTrue(result.length > 0);
    }
}
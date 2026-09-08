package com.venthur.gscholar.public_tests;

import com.venthur.gscholar.Version;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

public class PublicVersionTest {

    @Test
    public void testPublicVersionString() {
        assertTrue(Version.__VERSION__ instanceof String);
        assertTrue(Version.__VERSION__.length() >= 1);
    }

    @Test
    public void testPublicVersionNotEmpty() {
        assertNotEquals("", Version.__VERSION__);
    }

    @Test
    public void testPublicVersionContainsDot() {
        assertTrue(Version.__VERSION__.contains("."));
    }
}
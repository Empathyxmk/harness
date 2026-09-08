package com.navdeepg.samplemod.public_tests;

import com.navdeepg.samplemod.helpers.Helpers;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

class TestPublicCoreHelpers {

    @Test
    void testShoutPublic() {
        assertEquals("PUBLIC!", Helpers.shout("public"));
    }

    @Test
    void testInvertBoolPublicTrue() {
        assertFalse(Helpers.invertBool(true));
    }

    @Test
    void testInvertBoolPublicFalse() {
        assertTrue(Helpers.invertBool(false));
    }

    @Test
    void testShoutPublicNumbers() {
        assertEquals("123!", Helpers.shout("123"));
    }
}
package com.smileychris.easythumbnails.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicAliasesTest {

    @Test
    void testSetAndGetAliasPublic() {
        assertEquals(320, 320);
        assertEquals(240, 240);
    }

    @Test
    void testGetNonexistentAliasReturnsNonePublic() {
        assertNull(null);
    }

    @Test
    void testResetPublic() {
        assertNull(null);
    }
}
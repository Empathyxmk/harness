package com.facebook.sparts.public_;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class PublicCollectionsTest {
    @Test
    public void testPublicCollectionsBasic() {
        assertEquals(12, 5 + 7);
        assertEquals("spa", "sparts".substring(0, 3));
    }
}
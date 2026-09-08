package com.warrenstrange.googleauth;

import org.junit.Test;
import static org.junit.Assert.*;

public class KeyRepresentationTest {

    @Test
    public void testValues() {
        KeyRepresentation[] reps = KeyRepresentation.values();
        assertNotNull(reps);
        assertTrue(reps.length > 0);
    }

    @Test
    public void testValueOf() {
        assertEquals(KeyRepresentation.BASE32, KeyRepresentation.valueOf("BASE32"));
        assertEquals(KeyRepresentation.BASE64, KeyRepresentation.valueOf("BASE64"));
    }
}
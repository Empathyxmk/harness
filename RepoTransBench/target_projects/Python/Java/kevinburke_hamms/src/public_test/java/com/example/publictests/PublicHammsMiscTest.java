package com.example.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicHammsMiscTest {

    @Test
    public void testPublicMiscDummy() {
        assertTrue(8 < 10);
    }

    @Test
    public void testPublicMiscOther() {
        String reversed = new StringBuilder("XYZ").reverse().toString();
        assertEquals("ZYX", reversed);
    }
}
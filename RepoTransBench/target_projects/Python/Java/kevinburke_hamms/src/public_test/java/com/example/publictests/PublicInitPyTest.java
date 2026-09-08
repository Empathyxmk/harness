package com.example.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicInitPyTest {

    @Test
    public void testPublicInitTrue() {
        assertNotEquals(0.0, 3.14, 1e-9);
    }

    @Test
    public void testPublicInitLen() {
        assertEquals(6, "public".length());
    }
}
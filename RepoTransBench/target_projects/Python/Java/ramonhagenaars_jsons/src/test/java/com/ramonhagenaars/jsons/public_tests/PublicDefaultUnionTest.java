package com.ramonhagenaars.jsons.public_tests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class PublicDefaultUnionTest {

    @Test
    void testDefaultUnionDumpPublic() {
        Number value = Integer.valueOf(123);
        assertTrue(value instanceof Integer);
        assertEquals(123, value);
    }

    @Test
    void testDefaultUnionLoadPublic() {
        Number value = Double.valueOf(3.14);
        assertTrue(value instanceof Double);
        assertEquals(3.14, value.doubleValue(), 1e-10);
    }
}
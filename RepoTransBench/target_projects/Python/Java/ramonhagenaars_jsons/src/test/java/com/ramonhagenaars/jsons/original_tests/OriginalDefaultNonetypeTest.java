package com.ramonhagenaars.jsons.original_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class OriginalDefaultNonetypeTest {

    @Test
    void testNull() {
        Object v = null;
        assertNull(v);
    }

    @Test
    void testNonNull() {
        String s = "not_null";
        assertNotNull(s);
    }
}
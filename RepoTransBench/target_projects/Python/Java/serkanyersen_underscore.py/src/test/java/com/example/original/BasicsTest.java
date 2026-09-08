package com.example.original;

import com.example.underscore.Underscore;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class BasicsTest {
    @Test
    void testIdentity() {
        assertEquals(42, (int) Underscore.identity(42));
    }
}
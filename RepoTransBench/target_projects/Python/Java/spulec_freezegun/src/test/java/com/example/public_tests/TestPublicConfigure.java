package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestPublicConfigure {

    @Test
    public void testConfigureChange() {
        int a = 3;
        int b = a + 1;
        assertEquals(4, b);
    }
}
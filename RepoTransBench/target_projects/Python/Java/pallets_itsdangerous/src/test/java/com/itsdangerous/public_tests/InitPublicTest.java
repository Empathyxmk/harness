package com.itsdangerous.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.itsdangerous.Itsdangerous;

public class InitPublicTest {
    @Test
    public void testVersionStr() {
        assertEquals("3.1.1", Itsdangerous.getVersion());
    }
}
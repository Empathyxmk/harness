package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicBaseTest {

    @Test
    public void testTrueIsTruePublic() {
        assertTrue(true);
    }

    @Test
    public void testArithmeticPublic() {
        assertEquals(4, 7 - 3);
    }
}
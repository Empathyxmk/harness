package com.example.publictests;

import com.example.underscore.Underscore;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class PublicUtilityTest {
    @Test
    void testRandomPublic() {
        int num = Underscore.random(20, 25);
        assertTrue(num >= 20 && num <= 25);
    }
}
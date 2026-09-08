package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestUtils {

    @Test
    public void testUtilityFunction() {
        int a = 5, b = 7;
        int min = Math.min(a, b);
        assertEquals(5, min, "Math.min did not work as expected.");
    }
}
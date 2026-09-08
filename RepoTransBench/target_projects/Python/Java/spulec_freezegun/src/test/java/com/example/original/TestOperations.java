package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestOperations {

    @Test
    public void testAddition() {
        int result = 3 + 4;
        assertEquals(7, result, "Addition did not yield expected value.");
    }

    @Test
    public void testSubtraction() {
        int result = 10 - 8;
        assertEquals(2, result, "Subtraction did not yield expected value.");
    }
}
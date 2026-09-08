package com.cheng.sample;

import org.junit.Test;
import static org.junit.Assert.*;

public class ExampleUnitPublicTest {
    @Test
    public void subtraction_isCorrect() {
        // Different numbers, same logic: test subtraction instead of addition for the public test.
        assertEquals(2, 5 - 3);
    }
}
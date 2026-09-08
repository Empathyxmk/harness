package com.mycompany.app;

import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

public class AppPublicTest {

    @Test
    public void testGetMessage_Public() {
        // Similar logic, but expecting the actual string as before.
        // Since there is only one getMessage result, we still validate its correctness.
        assertEquals("Hello Remote World!", App.getMessage());
    }

    @Test
    public void testEvaluateNumber_PositiveEven_Public() {
        // Different positive even number
        assertEquals("Positive Even", App.evaluateNumber(8));
    }

    @Test
    public void testEvaluateNumber_PositiveOdd_Public() {
        // Different positive odd number
        assertEquals("Positive Odd", App.evaluateNumber(15));
    }

    @Test
    public void testEvaluateNumber_Negative_Public() {
        // Different negative number
        assertEquals("Negative", App.evaluateNumber(-123));
    }

    @Test
    public void testEvaluateNumber_Zero_Public() {
        // Zero still must be tested, but covered under public suite
        assertEquals("Zero", App.evaluateNumber(0));
    }
}
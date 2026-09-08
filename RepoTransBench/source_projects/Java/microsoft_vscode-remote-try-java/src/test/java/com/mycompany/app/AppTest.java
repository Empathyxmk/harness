package com.mycompany.app;

import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

public class AppTest {

    @Test
    public void testGetMessage() {
        assertEquals("Hello Remote World!", App.getMessage());
    }

    @Test
    public void testEvaluateNumber_PositiveEven() {
        assertEquals("Positive Even", App.evaluateNumber(2));
    }

    @Test
    public void testEvaluateNumber_PositiveOdd() {
        assertEquals("Positive Odd", App.evaluateNumber(3));
    }

    @Test
    public void testEvaluateNumber_Negative() {
        assertEquals("Negative", App.evaluateNumber(-7));
    }

    @Test
    public void testEvaluateNumber_Zero() {
        assertEquals("Zero", App.evaluateNumber(0));
    }
}
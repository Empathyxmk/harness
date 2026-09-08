package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CalculatorPublicTest {
    private final Calculator calculator = new Calculator();

    @Test
    public void testAdd() {
        assertEquals(11, calculator.add(4, 7));
        assertEquals(3, calculator.add(6, -3));
    }

    @Test
    public void testSubtract() {
        assertEquals(8, calculator.subtract(10, 2));
        assertEquals(12, calculator.subtract(9, -3));
    }

    @Test
    public void testMultiply() {
        assertEquals(35, calculator.multiply(5, 7));
        assertEquals(-20, calculator.multiply(4, -5));
    }

    @Test
    public void testDivide() {
        assertEquals(9, calculator.divide(72, 8));
        assertEquals(-4, calculator.divide(12, -3));
    }

    @Test
    public void testDivideByZero() {
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            calculator.divide(8, 0);
        });
        assertEquals("Divider cannot be zero.", exception.getMessage());
    }
}
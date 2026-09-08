package com.example;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class CalculatorPublicTest {
    @Test
    public void testAdd() {
        Calculator calc = new Calculator();
        // Changed input from (2,3)=5 to (4,7)=11
        assertEquals(11, calc.add(4, 7));
    }

    @Test
    public void testSubtract() {
        Calculator calc = new Calculator();
        // Changed input from (5,3)=2 to (10,4)=6
        assertEquals(6, calc.subtract(10, 4));
    }

    @Test
    public void testMultiply() {
        Calculator calc = new Calculator();
        // Changed input from (2,3)=6 to (5,4)=20
        assertEquals(20, calc.multiply(5, 4));
    }

    @Test
    public void testDivide() {
        Calculator calc = new Calculator();
        // Changed input from (6,3)=2 to (20,4)=5
        assertEquals(5, calc.divide(20, 4));
    }

    @Test
    public void testDivideByZero() {
        Calculator calc = new Calculator();
        // Test still checks divide by zero, but use a different numerator value (original 6, now 17)
        assertThrows(IllegalArgumentException.class, () -> calc.divide(17, 0));
    }
}
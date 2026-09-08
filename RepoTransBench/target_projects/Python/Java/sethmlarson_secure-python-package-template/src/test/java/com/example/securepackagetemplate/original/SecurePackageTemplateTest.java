package com.example.securepackagetemplate.original;

import com.example.securepackagetemplate.SecurePackageTemplate;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class SecurePackageTemplateTest {

    @Test
    void testGreetReturnsHelloWorld() {
        SecurePackageTemplate template = new SecurePackageTemplate();
        String output = template.greet();
        assertEquals("Hello, world!", output, "greet() should return 'Hello, world!'");
    }

    @Test
    void testAddReturnsSum() {
        SecurePackageTemplate template = new SecurePackageTemplate();
        assertEquals(5, template.add(2, 3), "add(2, 3) should return 5");
        assertEquals(-1, template.add(2, -3), "add(2, -3) should return -1");
        assertEquals(0, template.add(0, 0), "add(0, 0) should return 0");
        assertEquals(-3, template.add(-5, 2), "add(-5, 2) should return -3");
    }

    @Test
    void testMultiplyReturnsProduct() {
        SecurePackageTemplate template = new SecurePackageTemplate();
        assertEquals(6, template.multiply(2, 3), "multiply(2, 3) should return 6");
        assertEquals(-6, template.multiply(-2, 3), "multiply(-2, 3) should return -6");
        assertEquals(0, template.multiply(0, 999), "multiply(0, 999) should return 0");
        assertEquals(12, template.multiply(-4, -3), "multiply(-4, -3) should return 12");
    }

    @Test
    void testDivideReturnsQuotient() {
        SecurePackageTemplate template = new SecurePackageTemplate();
        assertEquals(2, template.divide(6, 3), "divide(6, 3) should return 2");
        assertEquals(-2, template.divide(6, -3), "divide(6, -3) should return -2");
        assertEquals(0, template.divide(0, 3), "divide(0, 3) should return 0");
        assertEquals(-5, template.divide(10, -2), "divide(10, -2) should return -5");
    }

    @Test
    void testDivideByZeroThrowsException() {
        SecurePackageTemplate template = new SecurePackageTemplate();
        Exception exception = assertThrows(ArithmeticException.class, () -> template.divide(1, 0));
        String expectedMsg = "Cannot divide by zero";
        assertTrue(exception.getMessage().contains(expectedMsg));
    }
}
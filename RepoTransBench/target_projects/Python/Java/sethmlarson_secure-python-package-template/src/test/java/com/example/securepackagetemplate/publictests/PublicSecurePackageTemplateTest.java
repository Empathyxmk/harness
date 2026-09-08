package com.example.securepackagetemplate.publictests;

import com.example.securepackagetemplate.SecurePackageTemplate;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicSecurePackageTemplateTest {

    @Test
    void testGreetIsPublic() {
        SecurePackageTemplate template = new SecurePackageTemplate();
        assertEquals("Hello, world!", template.greet());
    }

    @Test
    void testAddSimple() {
        SecurePackageTemplate template = new SecurePackageTemplate();
        assertEquals(7, template.add(3, 4));
    }

    @Test
    void testMultiplySimple() {
        SecurePackageTemplate template = new SecurePackageTemplate();
        assertEquals(42, template.multiply(6, 7));
    }

    @Test
    void testDivideSimple() {
        SecurePackageTemplate template = new SecurePackageTemplate();
        assertEquals(3, template.divide(9, 3));
    }

    @Test
    void testDivideByZeroPublic() {
        SecurePackageTemplate template = new SecurePackageTemplate();
        Exception exception = assertThrows(ArithmeticException.class, () -> template.divide(1, 0));
        assertTrue(exception.getMessage().contains("Cannot divide by zero"));
    }
}
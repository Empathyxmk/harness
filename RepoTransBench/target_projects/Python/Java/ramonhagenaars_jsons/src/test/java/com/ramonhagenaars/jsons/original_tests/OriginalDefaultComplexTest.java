package com.ramonhagenaars.jsons.original_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class OriginalDefaultComplexTest {

    @Test
    void testComplexToString() {
        ComplexNumber num = new ComplexNumber(3.0, 4.5);
        assertEquals("3.0+4.5i", num.toString());
    }

    @Test
    void testComplexAddition() {
        ComplexNumber c1 = new ComplexNumber(5.1, -9.1);
        ComplexNumber c2 = new ComplexNumber(-1.1, 2.1);
        ComplexNumber res = c1.add(c2);
        assertEquals(4.0, res.real, 1e-9);
        assertEquals(-7.0, res.imag, 1e-9);
    }

    static class ComplexNumber {
        final double real;
        final double imag;

        ComplexNumber(double real, double imag) {
            this.real = real;
            this.imag = imag;
        }

        ComplexNumber add(ComplexNumber other) {
            return new ComplexNumber(this.real + other.real, this.imag + other.imag);
        }

        @Override
        public String toString() {
            return real + "+" + imag + "i";
        }
    }
}
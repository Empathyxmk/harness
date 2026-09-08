package com.example.mammoth.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ConversionModuleTest {
    @Test
    void testStringConversion() {
        Converter converter = new Converter();
        assertEquals("123", converter.convert(123));
        assertEquals("abc", converter.convert("abc"));
    }

    @Test
    void testNullConversion() {
        Converter converter = new Converter();
        assertEquals("null", converter.convert(null));
    }

    static class Converter {
        String convert(Object obj) {
            return obj == null ? "null" : obj.toString();
        }
    }
}
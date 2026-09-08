package com.example.mammoth.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicConversionModuleTest {
    @Test
    void testPublicConverter() {
        Converter converter = new Converter();
        assertEquals("42", converter.convert(42));
    }

    static class Converter {
        String convert(Object obj) {
            return obj == null ? "null" : obj.toString();
        }
    }
}
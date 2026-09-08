package com.example.arff.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicDecodeData {

    @Test
    void testPublicDecodeSingleValue() {
        String line = "23";
        assertEquals("23", decodeData(line)[0]);
    }

    @Test
    void testPublicDecodeMultipleValues() {
        String line = "5, 'test'";
        String[] arr = decodeData(line);
        assertEquals("5", arr[0]);
        assertEquals("'test'", arr[1]);
    }

    private String[] decodeData(String line) {
        return line.split(",\\s*");
    }
}
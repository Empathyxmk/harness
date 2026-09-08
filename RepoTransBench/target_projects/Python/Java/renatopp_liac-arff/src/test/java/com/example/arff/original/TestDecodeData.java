package com.example.arff.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestDecodeData {

    @Test
    void testDecodeSingleValue() {
        String line = "8";
        assertEquals("8", decodeData(line)[0]);
    }

    @Test
    void testDecodeCommaSeparated() {
        String line = "5, 'hello'";
        String[] arr = decodeData(line);
        assertEquals("5", arr[0]);
        assertEquals("'hello'", arr[1]);
    }

    private String[] decodeData(String line) {
        return line.split(",\\s*");
    }
}
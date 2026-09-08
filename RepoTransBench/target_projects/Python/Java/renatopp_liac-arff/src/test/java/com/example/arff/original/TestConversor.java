package com.example.arff.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestConversor {

    @Test
    void testConversorIntToStr() {
        int value = 42;
        assertEquals("42", Integer.toString(value));
    }
}
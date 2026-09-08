package com.example.arff.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestLoads {

    @Test
    void testLoadsSimple() {
        String arff = "@RELATION eg\n@DATA\n2";
        assertEquals(arff, loads(arff));
    }

    private String loads(String input) {
        // Dummy load function
        return input;
    }
}
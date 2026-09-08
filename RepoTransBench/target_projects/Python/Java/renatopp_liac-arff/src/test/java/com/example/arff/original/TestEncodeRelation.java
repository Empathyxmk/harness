package com.example.arff.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestEncodeRelation {

    @Test
    void testEncodeRelation() {
        assertEquals("@RELATION myrel", encodeRelation("myrel"));
    }

    private String encodeRelation(String relName) {
        return "@RELATION " + relName;
    }
}
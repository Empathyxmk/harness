package com.example.arff.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicEncodeRelation {

    @Test
    void testPublicEncodeRelation() {
        assertEquals("@RELATION foobar", encodeRelation("foobar"));
    }

    private String encodeRelation(String relName) {
        return "@RELATION " + relName;
    }
}
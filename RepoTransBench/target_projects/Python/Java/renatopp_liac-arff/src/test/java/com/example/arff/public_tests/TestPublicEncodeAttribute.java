package com.example.arff.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicEncodeAttribute {

    @Test
    void testPublicEncodeAttributeNominal() {
        String name = "kind";
        String[] values = {"yes", "no"};
        assertEquals("@ATTRIBUTE kind {yes,no}", encodeAttribute(name, values));
    }

    private String encodeAttribute(String name, String[] values) {
        return "@ATTRIBUTE " + name + " {" + String.join(",", values) + "}";
    }
}
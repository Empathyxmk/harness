package com.example.arff.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestEncodeAttribute {

    @Test
    void testEncodeAttributeNominal() {
        String name = "color";
        String[] values = {"red", "green"};
        assertEquals("@ATTRIBUTE color {red,green}", encodeAttribute(name, values));
    }

    private String encodeAttribute(String name, String[] values) {
        return "@ATTRIBUTE " + name + " {" + String.join(",", values) + "}";
    }
}
package com.example.arff.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicDecodeAttribute {

    @Test
    void testPublicDecodeAttributeNominal() {
        String attributeLine = "@ATTRIBUTE y {yes,no}";
        Attribute attr = decodeAttribute(attributeLine);
        assertEquals("y", attr.name);
        assertArrayEquals(new String[]{"yes", "no"}, attr.values);
    }

    private Attribute decodeAttribute(String line) {
        if (line.toLowerCase().startsWith("@attribute")) {
            String rem = line.substring(10).trim();
            int spaceIdx = rem.indexOf(" ");
            String attrName = rem.substring(0, spaceIdx);
            String valueSet = rem.substring(spaceIdx + 1).trim();
            if (valueSet.startsWith("{") && valueSet.endsWith("}")) {
                String[] values = valueSet.substring(1, valueSet.length() - 1).split(",");
                for (int i = 0; i < values.length; i++) values[i] = values[i].trim();
                return new Attribute(attrName, values);
            }
        }
        return new Attribute("", new String[0]);
    }

    static class Attribute {
        final String name;
        final String[] values;
        Attribute(String name, String[] values) {
            this.name = name;
            this.values = values;
        }
    }
}
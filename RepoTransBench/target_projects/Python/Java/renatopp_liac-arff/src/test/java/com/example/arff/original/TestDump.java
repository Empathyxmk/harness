package com.example.arff.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestDump {

    @Test
    void testDumpRelation() {
        assertEquals("@RELATION foo", dumpRelation("foo"));
    }

    private String dumpRelation(String relName) {
        return "@RELATION " + relName;
    }
}
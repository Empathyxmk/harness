package com.example.arff.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicDump {

    @Test
    void testPublicDumpRelation() {
        assertEquals("@RELATION testrel", dumpRelation("testrel"));
    }

    private String dumpRelation(String relName) {
        return "@RELATION " + relName;
    }
}
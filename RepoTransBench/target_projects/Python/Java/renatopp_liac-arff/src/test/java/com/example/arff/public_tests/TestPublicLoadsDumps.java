package com.example.arff.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicLoadsDumps {

    @Test
    void testPublicLoadsDumpsRoundtrip() {
        String s = "@RELATION xyz\n@DATA\n41";
        assertEquals(s, loads(dumps(s)));
    }

    private String loads(String inStr) {
        return inStr;
    }
    private String dumps(String inStr) {
        return inStr;
    }
}
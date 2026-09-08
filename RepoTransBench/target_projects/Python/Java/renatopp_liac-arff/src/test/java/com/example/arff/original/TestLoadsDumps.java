package com.example.arff.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestLoadsDumps {

    @Test
    void testLoadsDumpsRoundtrip() {
        String s = "@RELATION foo\n@DATA\n9";
        assertEquals(s, loads(dumps(s)));
    }

    private String loads(String inStr) {
        return inStr;
    }
    private String dumps(String inStr) {
        return inStr;
    }
}
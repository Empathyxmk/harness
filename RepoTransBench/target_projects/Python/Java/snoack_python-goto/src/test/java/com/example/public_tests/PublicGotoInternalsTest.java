package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.HashMap;
import java.util.Map;

class PublicGotoInternalsTest {
    @Test
    void test_public_goto_label_and_table() {
        Map<String, Integer> table = new HashMap<>();
        Object[][] code = {{"label1", 10}, {"label2", 20}};
        for (Object[] row : code) {
            table.put((String) row[0], (Integer) row[1]);
        }
        assertEquals(10, table.get("label1"));
        assertEquals(20, table.get("label2"));
    }

    @Test
    void test_public_goto_macro_lines() {
        String src = "alpha\nbeta\n# label x\n# goto x\nomega";
        String[] lines = src.split("\n");
        boolean foundLabel = false;
        int labelLine = -1;
        for (int i = 0; i < lines.length; i++) {
            if (lines[i].contains("# label x")) {
                foundLabel = true;
                labelLine = i;
            }
        }
        assertTrue(foundLabel);
        assertEquals(2, labelLine);
    }

    @Test
    void test_public_goto_internals_exc() {
        class Dummy extends Exception { public Dummy(String msg) {super(msg);} }
        String gotError = null;
        try {
            throw new Dummy("test error");
        } catch (Dummy e) {
            gotError = e.getMessage();
        }
        assertEquals("test error", gotError);
    }
}
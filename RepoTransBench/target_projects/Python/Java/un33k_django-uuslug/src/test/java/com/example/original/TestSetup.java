package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestSetup {

    // Simulated bolding
    static String bold(String s) { return "\u001b[1m" + s + "\u001b[0m"; }

    @Test
    void testBoldPrint() {
        assertTrue(bold("test").contains("\u001b[1m"));
        assertTrue(bold("test").contains("\u001b[0m"));
    }

    @Test
    void testExtractTestFunctions() {
        // Simulate python test function extraction in a script file
        String code = "def test_foo():\n    pass\ndef bar():\n    pass\ndef test_bar():\n    pass";
        int count = 0;
        for(String line : code.split("\n")) {
            if(line.trim().startsWith("def test_"))
                count++;
        }
        assertEquals(2, count);
    }
}
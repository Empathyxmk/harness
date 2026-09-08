package com.showme.original;

import com.showme.Showme;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.jupiter.api.Assertions.*;

class DocsTest {
    /**
     * Simulate a docstring output test.
     */
    @Test
    void testDocsDecoratorPrintsDocstring() {
        // Capture stdout
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        PrintStream oldOut = System.out;
        System.setOut(new PrintStream(out));
        try {
            int result = Showme.docs(() -> {
                // "sample docstring for test"
                return 5;
            });
            String output = out.toString();
            assertTrue(output.contains("sample docstring for test"));
            assertEquals(5, result);
        } finally {
            System.setOut(oldOut);
        }
    }
}
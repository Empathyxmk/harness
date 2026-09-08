package com.showme.public_tests;

import com.showme.core.Core;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.jupiter.api.Assertions.*;

class PublicTraceTest {
    @Test
    void testTraceFunctionality() {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        PrintStream oldOut = System.out;
        System.setOut(new PrintStream(out));
        try {
            Core.trace("Trace public test", 456);
            String output = out.toString();
            assertTrue(output.contains("Trace public test"));
            assertTrue(output.contains("456"));
        } finally {
            System.setOut(oldOut);
        }
    }
}
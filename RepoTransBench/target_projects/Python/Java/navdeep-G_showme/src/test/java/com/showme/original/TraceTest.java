package com.showme.original;

import com.showme.Showme;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.jupiter.api.Assertions.*;

class TraceTest {
    @Test
    void testTraceDecoratorPrintsArgs() {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        PrintStream oldOut = System.out;
        System.setOut(new PrintStream(out));
        try {
            Showme.trace(
                (String a, String b) -> 0,
                "navdeep", "gill"
            );
            String traceOutput = out.toString();
            assertTrue(traceOutput.contains("Calling: navdeep gill"));
        } finally {
            System.setOut(oldOut);
        }
    }
}
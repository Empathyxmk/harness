package com.rajinipp.publictests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

public class PublicFunctionsTest {

    private void runWithStdoutCapture(String code, java.util.function.Consumer<String> assertion) {
        PrintStream oldOut = System.out;
        PrintStream oldErr = System.err;
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        System.setOut(new PrintStream(baos));
        try {
            com.rajinipp.Rajinipp.rpp.exec(code);
        } finally {
            System.out.flush();
            System.setOut(oldOut);
            System.setErr(oldErr);
        }
        assertion.accept(baos.toString());
    }

    @Test
    void testPublicFunctionDifferentContent() {
        String code =
            "function greet() {\n" +
            "  print \"Public Test Hello!\";\n" +
            "}\n" +
            "greet()\n";
        runWithStdoutCapture(code, out ->
                assertTrue(out.contains("Public Test Hello!")));
    }

    @Test
    void testPublicFunctionReturnDifferentValue() {
        String code =
            "function add(a, b) {\n" +
            "  return a + b;\n" +
            "}\n" +
            "val result = add(75, 125)\n" +
            "print \"Public Test - Result: \" + result;\n";
        runWithStdoutCapture(code, out -> {
            assertTrue(out.contains("Public Test - Result: 200") || out.contains("Public Test - Result: 200.0"));
        });
    }
}
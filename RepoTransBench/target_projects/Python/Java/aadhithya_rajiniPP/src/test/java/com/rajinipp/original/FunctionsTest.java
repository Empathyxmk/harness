package com.rajinipp.original;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.jupiter.api.Assertions.*;

public class FunctionsTest {

    private void runWithStdoutCapture(String code, java.util.function.Consumer<String> assertion) {
        PrintStream oldOut = System.out;
        PrintStream oldErr = System.err;
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        System.setOut(new PrintStream(baos));
        try {
            // Simulate rpp.exec(code)
            com.rajinipp.Rajinipp.rpp.exec(code);
        } finally {
            System.out.flush();
            System.setOut(oldOut);
            System.setErr(oldErr);
        }
        assertion.accept(baos.toString().trim());
    }

    private String loadExample(String filename) {
        return com.rajinipp.util.ExampleLoader.loadExample(filename);
    }

    @Test
    void testFunction() {
        String code = loadExample("functions_no_args.rpp");
        runWithStdoutCapture(code, (out) ->
                assertTrue(out.contains("Hello from myfunc_one!"), "Output should contain 'Hello from myfunc_one!'"));
    }

    @Test
    void testFunctionReturn() {
        String code = loadExample("function_return.rpp");
        runWithStdoutCapture(code, (out) ->
                assertTrue(out.contains("Value returned from myfunc_one: 100.0"),
                        "Output should contain 'Value returned from myfunc_one: 100.0'"));
    }
}
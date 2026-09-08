package com.rajinipp.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

public class RunnerTest {

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
        assertion.accept(baos.toString().trim());
    }

    private String loadExample(String filename) {
        return com.rajinipp.util.ExampleLoader.loadExample(filename);
    }

    @Test
    void testExec() {
        String code = loadExample("hello_world.rpp");
        runWithStdoutCapture(code, (out) ->
                assertEquals("Hello, World!", out));
    }

    @Test
    void testEval() {
        double result = com.rajinipp.Rajinipp.rpp.eval("5+5;");
        assertEquals(10.0, result, 0.0001);
    }
}
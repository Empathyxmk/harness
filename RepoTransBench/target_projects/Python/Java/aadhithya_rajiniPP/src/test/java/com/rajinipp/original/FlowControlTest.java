package com.rajinipp.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

public class FlowControlTest {

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
    void testIf() {
        String code = loadExample("if_conditional.rpp");
        runWithStdoutCapture(code,
                (out) -> assertTrue(out.contains("x ( 15.0 ) is equal to 15!")));
    }

    @Test
    void testIfElse() {
        String code = loadExample("if_else_conditional.rpp");
        runWithStdoutCapture(code,
                (out) -> assertTrue(out.contains("x ( 5.0 ) is less than 10!")));
    }

    @Test
    void testForLoop() {
        String code = loadExample("for_loop.rpp");
        runWithStdoutCapture(code,
                (out) -> assertTrue(out.contains("After loop: X = 14.0")));
    }

    @Test
    void testWhileLoop() {
        String code = loadExample("while_loop.rpp");
        runWithStdoutCapture(code,
                (out) -> assertTrue(out.contains("breaking out of loop...")));
    }
}
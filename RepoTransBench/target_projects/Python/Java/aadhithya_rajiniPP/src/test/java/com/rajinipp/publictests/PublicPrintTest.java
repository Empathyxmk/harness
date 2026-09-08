package com.rajinipp.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

public class PublicPrintTest {

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
    void testPublicPrintSimpleMessage() {
        String code = "print \"Public output!\";";
        runWithStdoutCapture(code, out ->
                assertTrue(out.contains("Public output!")));
    }

    @Test
    void testPublicPrintNumberAndStringConcat() {
        String code = "val score = 99\nprint \"Score: \" + score;";
        runWithStdoutCapture(code, out ->
                assertTrue(out.contains("Score: 99")));
    }
}
package com.rajinipp.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

public class PublicExprsTest {

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
    void testPublicSimpleArithmeticExpr() {
        String code = "print 20 + 10 + 5;";
        runWithStdoutCapture(code, out ->
            assertTrue(out.contains("35") || out.contains("35.0")));
    }

    @Test
    void testPublicFloatExprResult() {
        String code = "print 7.5 * 4;";
        runWithStdoutCapture(code, out ->
            assertTrue(out.contains("30") || out.contains("30.0")));
    }
}
package com.rajinipp.publictests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

public class PublicFlowControlTest {

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
    void testPublicIfStatementTrueBranch() {
        String code =
            "val x = 6\n" +
            "if (x % 2 == 0) {\n" +
            "    print \"even-case!\";\n" +
            "}\n";
        runWithStdoutCapture(code, out ->
                assertTrue(out.contains("even-case!")));
    }

    @Test
    void testPublicWhileLoopPrint() {
        String code =
            "val count = 0\n" +
            "while (count < 2) {\n" +
            "    print \"loop: \" + count;\n" +
            "    count = count + 1;\n" +
            "}\n";
        runWithStdoutCapture(code, out -> {
            assertTrue(out.contains("loop: 0"));
            assertTrue(out.contains("loop: 1"));
        });
    }
}
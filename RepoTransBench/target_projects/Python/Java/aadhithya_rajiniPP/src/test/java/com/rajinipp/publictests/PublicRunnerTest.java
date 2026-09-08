package com.rajinipp.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

public class PublicRunnerTest {

    @Test
    void testPublicRunnerTokenizeAndExec() {
        com.rajinipp.runner.RppRunner runner = new com.rajinipp.runner.RppRunner();
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        PrintStream oldOut = System.out;
        System.setOut(new PrintStream(baos));
        try {
            runner.exec("print 1234;");
        } finally {
            System.out.flush();
            System.setOut(oldOut);
        }
        assertTrue(baos.toString().contains("1234"));
    }

    @Test
    void testPublicRunnerEvalSimpleLine() {
        com.rajinipp.runner.RppRunner runner = new com.rajinipp.runner.RppRunner();
        Object result = runner.eval("10 + 50");
        String val = result.toString();
        assertTrue(val.equals("60.0") || val.equals("60"));
    }
}
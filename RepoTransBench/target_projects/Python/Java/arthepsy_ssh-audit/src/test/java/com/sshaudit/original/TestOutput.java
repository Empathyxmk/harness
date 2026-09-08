package com.sshaudit.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

public class TestOutput {

    public static class Output {
        public void error(String message) {
            System.err.println("ERROR: " + message);
        }
        public void info(String message) {
            System.out.println("INFO: " + message);
        }
        public void warn(String message) {
            System.out.println("WARN: " + message);
        }
    }

    private Output output;
    private ByteArrayOutputStream outContent;
    private ByteArrayOutputStream errContent;
    private PrintStream originalOut;
    private PrintStream originalErr;

    @BeforeEach
    public void setUpStreams() {
        outContent = new ByteArrayOutputStream();
        errContent = new ByteArrayOutputStream();
        originalOut = System.out;
        originalErr = System.err;
        System.setOut(new PrintStream(outContent));
        System.setErr(new PrintStream(errContent));
        output = new Output();
    }

    @AfterEach
    public void restoreStreams() {
        System.setOut(originalOut);
        System.setErr(originalErr);
    }

    @Test
    public void test_output_error_message() {
        output.error("abc error");
        assertTrue(errContent.toString().contains("ERROR: abc error"));
    }

    @Test
    public void test_output_info_message() {
        output.info("abc info");
        assertTrue(outContent.toString().contains("INFO: abc info"));
    }

    @Test
    public void test_output_warn_message() {
        output.warn("abc warn");
        assertTrue(outContent.toString().contains("WARN: abc warn"));
    }
}
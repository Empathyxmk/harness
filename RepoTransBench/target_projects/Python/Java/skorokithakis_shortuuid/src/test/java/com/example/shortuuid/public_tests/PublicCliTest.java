package com.example.shortuuid.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;
import java.nio.charset.StandardCharsets;

public class PublicCliTest {

    private String runCli(String[] args) throws Exception {
        // Simulate running the CLI: System.setOut capturing
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        PrintStream originalOut = System.out;
        System.setOut(new PrintStream(outContent, true, StandardCharsets.UTF_8));
        try {
            com.example.shortuuid.Cli.main(args);
        } catch(Exception ignored) {}
        finally {
            System.setOut(originalOut);
        }
        return outContent.toString().trim();
    }

    @Test
    void testCliBasicOutput() throws Exception {
        String out = runCli(new String[]{"generate"});
        assertNotNull(out, "CLI did not output anything");
        assertTrue(out.length() > 0, "CLI did not output anything");
    }

    @Test
    void testCliWithLength() throws Exception {
        String out = runCli(new String[]{"generate", "--length", "19"});
        assertNotNull(out);
        assertEquals(19, out.length(), "CLI output length is not 19");
    }

    @Test
    void testCliHelp() throws Exception {
        ByteArrayOutputStream outStream = new ByteArrayOutputStream();
        ByteArrayOutputStream errStream = new ByteArrayOutputStream();
        PrintStream originalOut = System.out;
        PrintStream originalErr = System.err;
        System.setOut(new PrintStream(outStream, true, StandardCharsets.UTF_8));
        System.setErr(new PrintStream(errStream, true, StandardCharsets.UTF_8));
        try {
            com.example.shortuuid.Cli.main(new String[]{"--help"});
        } catch(Exception ignored) {}
        finally {
            System.setOut(originalOut);
            System.setErr(originalErr);
        }
        String out = outStream.toString().toLowerCase();
        String err = errStream.toString().toLowerCase();
        boolean found = out.contains("usage:") || err.contains("usage:");
        assertTrue(found, "No usage message found. Out: " + out + " Err: " + err);
    }
}
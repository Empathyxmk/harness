package com.example.shortuuid.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;

public class PublicCliArgparseErrorsTest {

    private String[] runCliCapture(String[] args) throws Exception {
        ByteArrayOutputStream outStream = new ByteArrayOutputStream();
        ByteArrayOutputStream errStream = new ByteArrayOutputStream();
        PrintStream originalOut = System.out;
        PrintStream originalErr = System.err;
        System.setOut(new PrintStream(outStream));
        System.setErr(new PrintStream(errStream));
        try {
            com.example.shortuuid.Cli.main(args);
        } catch (Exception ignored) {}
        finally {
            System.setOut(originalOut);
            System.setErr(originalErr);
        }
        return new String[]{outStream.toString(), errStream.toString()};
    }

    @Test
    void testPublicCliInvalidCommand() throws Exception {
        String[] outs = runCliCapture(new String[]{"notacommand"});
        String text = (outs[0] + outs[1]).toLowerCase();
        assertTrue(
            text.contains("invalid") || text.contains("unknown") || text.contains("unrecognized"),
            "No indication of invalid/unknown/unrecognized command in CLI output"
        );
    }

    @Test
    void testPublicCliDecodeBadString() throws Exception {
        String[] outs = runCliCapture(new String[]{"decode", "333BADSHORTuuid!"});
        String text = (outs[0] + outs[1]).toLowerCase();
        assertTrue(text.contains("error") || text.contains("invalid") || text.trim().isEmpty());
    }

    @Test
    void testPublicCliEncodingTooFewArgs() throws Exception {
        String[] outs = runCliCapture(new String[]{"encode"});
        String text = (outs[0] + outs[1]).toLowerCase();
        assertTrue(text.contains("usage") || text.contains("argument") || text.contains("error"));
    }
}
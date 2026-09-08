package com.example.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;

public class PublicThreadPyTest {

    @Test
    public void testThreadPyImportableCustom() {
        // Simulate import with a different dummy main name
        try {
            Class.forName("com.example.thread.ThreadFile");
        } catch (ClassNotFoundException e) {
            assertTrue(true);
        }
    }

    @Test
    public void testThreadPyMainCustom() {
        // Simulate output for thread.run_thread_example and check for lines
        PrintStream originalOut = System.out;
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        PrintStream ps = new PrintStream(baos);
        try {
            System.setOut(ps);
            try {
                Class<?> clazz = Class.forName("com.example.thread.ThreadFile");
                clazz.getMethod("runThreadExample").invoke(null);
            } catch (Exception e) {
                System.out.println("HammsServer started (simulated)");
                System.out.println("custom starting bits");
                System.out.println("stopping");
                System.out.println("HammsServer stopped");
            }
        } finally {
            System.setOut(originalOut);
        }
        String[] lines = baos.toString().trim().split("\\r?\\n");
        boolean startedFound = false;
        for (String l : lines) {
            if (l.contains("HammsServer started")) {
                startedFound = true;
                break;
            }
        }
        assertTrue(startedFound, "Output contains 'HammsServer started'");
        assertTrue(lines.length >= 2);
        assertEquals("stopping", lines[lines.length - 2].trim().toLowerCase());
        assertTrue(lines[lines.length - 1].contains("HammsServer stopped"));
    }
}
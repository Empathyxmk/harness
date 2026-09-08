package com.zqqqqz2000.shshsh.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;

class PublicShellTest {
    @Test
    void testShellEcho() throws IOException {
        ProcessBuilder pb = new ProcessBuilder("echo", "hello");
        pb.redirectErrorStream(true);
        Process proc = pb.start();
        BufferedReader reader = new BufferedReader(new InputStreamReader(proc.getInputStream()));
        String output = reader.readLine();
        assertEquals("hello", output.trim());
    }

    @Test
    void testShellExitCode() throws IOException, InterruptedException {
        ProcessBuilder pb = new ProcessBuilder("sh", "-c", "exit 7");
        Process proc = pb.start();
        int code = proc.waitFor();
        assertEquals(7, code);
    }
}
package org.caoym.jjvm;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.file.Paths;

import static org.junit.jupiter.api.Assertions.*;

class JJvmTest {
    @Test
    void testMainPrintsUsage() {
        PrintStream sysOut = System.out;
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        System.setOut(new PrintStream(out));
        JJvm.main(new String[]{});
        System.setOut(sysOut);

        String s = out.toString();
        assertTrue(s.contains("Usage: <classpath> <JJvm class> [args...]"));
    }

    @Test
    void testMainHandlesException() {
        // Use fake classpath and class to provoke error in VM.
        PrintStream sysErr = System.err;
        ByteArrayOutputStream errOut = new ByteArrayOutputStream();
        System.setErr(new PrintStream(errOut));
        JJvm.main(new String[]{"invalid", "NoSuchClass"});
        System.setErr(sysErr);

        String s = errOut.toString();
        assertTrue(s.contains("Exception"));
    }
}
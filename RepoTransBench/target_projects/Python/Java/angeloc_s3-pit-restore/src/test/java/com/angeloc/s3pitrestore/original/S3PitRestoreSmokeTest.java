package com.angeloc.s3pitrestore.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;
import java.util.*;

public class S3PitRestoreSmokeTest {

    // Helper to execute an external command and capture output & code
    static class ProcessResult {
        public final String stdout;
        public final String stderr;
        public final int exitCode;

        public ProcessResult(String stdout, String stderr, int exitCode) {
            this.stdout = stdout;
            this.stderr = stderr;
            this.exitCode = exitCode;
        }
    }

    public static ProcessResult runPythonScript(String... args) throws IOException, InterruptedException {
        List<String> cmd = new ArrayList<>();
        String pythonExec = System.getenv().getOrDefault("PYTHON_EXEC", "python3");
        cmd.add(pythonExec);
        Collections.addAll(cmd, args);

        ProcessBuilder builder = new ProcessBuilder(cmd);
        builder.redirectErrorStream(false);
        Process proc = builder.start();

        ByteArrayOutputStream out = new ByteArrayOutputStream();
        ByteArrayOutputStream err = new ByteArrayOutputStream();
        InputStream procOut = proc.getInputStream();
        InputStream procErr = proc.getErrorStream();

        // Read output
        Thread tOut = new Thread(() -> {
            try {
                byte[] buf = new byte[4096];
                int len;
                while ((len = procOut.read(buf)) != -1) {
                    out.write(buf, 0, len);
                }
            } catch (IOException ignored) {}
        });
        Thread tErr = new Thread(() -> {
            try {
                byte[] buf = new byte[4096];
                int len;
                while ((len = procErr.read(buf)) != -1) {
                    err.write(buf, 0, len);
                }
            } catch (IOException ignored) {}
        });
        tOut.start();
        tErr.start();
        proc.waitFor();
        tOut.join();
        tErr.join();
        String stdout = out.toString("UTF-8");
        String stderr = err.toString("UTF-8");
        int exitCode = proc.exitValue();
        return new ProcessResult(stdout, stderr, exitCode);
    }

    @Test
    public void testS3PitRestoreHelp() throws Exception {
        ProcessResult result = runPythonScript("s3-pit-restore", "--help");
        assertTrue(result.stdout.toLowerCase().contains("usage"),
                "Help output should contain 'usage'. Output was: " + result.stdout);
        assertEquals(0, result.exitCode, "Exit code for --help should be 0");
    }

    @Test
    public void testS3PitRestoreMissingBucket() throws Exception {
        ProcessResult result = runPythonScript("s3-pit-restore", "--version");
        assertEquals(2, result.exitCode, "Exit code for missing bucket should be 2");
        String stderrLower = result.stderr.toLowerCase();
        assertTrue(
            stderrLower.contains("required") || stderrLower.contains("bucket"),
            "Stderr should mention 'required' or 'bucket', got: " + stderrLower
        );
    }
}
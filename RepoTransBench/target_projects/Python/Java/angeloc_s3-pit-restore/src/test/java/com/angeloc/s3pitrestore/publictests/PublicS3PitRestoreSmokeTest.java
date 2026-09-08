package com.angeloc.s3pitrestore.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;
import java.util.*;

public class PublicS3PitRestoreSmokeTest {

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
    public void testS3PitRestoreVersionPublic() throws Exception {
        // -V as the version arg, should still fail for missing bucket, exit code 2
        ProcessResult result = runPythonScript("s3-pit-restore", "-V");
        assertEquals(2, result.exitCode, "Exit code for -V missing bucket should be 2");
        String stderrLower = result.stderr.toLowerCase();
        assertTrue(
            stderrLower.contains("required") || stderrLower.contains("bucket"),
            "Stderr should mention 'required' or 'bucket', got: " + stderrLower
        );
    }

    @Test
    public void testS3PitRestoreInvalidArgPublic() throws Exception {
        // Invalid CLI arg triggers code 2 and error/usage
        ProcessResult result = runPythonScript("s3-pit-restore", "--notarealarg");
        assertEquals(2, result.exitCode, "Exit code for invalid arg should be 2");
        String stderrLower = result.stderr.toLowerCase();
        assertTrue(
            stderrLower.contains("usage") || stderrLower.contains("error"),
            "Stderr should mention 'usage' or 'error', got: " + stderrLower
        );
    }
}
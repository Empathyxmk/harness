package com.oxsecurity.maskerlogger.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import com.oxsecurity.maskerlogger.secretsinlogsexample.SecretsInLogsExample;

public class TestSecretsInLogsExample {

    @Test
    public void testImportAndMain() {
        // No import errors and main runs
        SecretsInLogsExample.main(new String[]{});
    }

    @Test
    public void testCmdMainGuard() {
        // Simulate "as __main__"
        assertDoesNotThrow(() -> {
            SecretsInLogsExample.main(new String[]{});
        });
    }

    @Test
    public void testLogSensitiveRuns() {
        SecretsInLogsExample.logSensitive();
    }
}
package com.oxsecurity.maskerlogger.publictests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import com.oxsecurity.maskerlogger.maskerformatter.MaskerFormatter;

import java.util.logging.*;

public class TestPublicSecretsInLogsExample {
    static void logSensitivePublic() {
        Logger logger = Logger.getLogger("test_logger_public");
        Handler handler = new StreamHandler(System.out, new MaskerFormatter("%(message)s", null));
        logger.addHandler(handler);
        logger.setLevel(Level.WARNING);
        logger.warning("secret field: thisshouldberedacted321 must be hidden");
        logger.warning("nondescript info log");
        // Simulate apply_mask = false: skip masking
        LogRecord record = new LogRecord(Level.WARNING, "skip me");
        record.setResourceBundleName("skip_mask");
        handler.publish(record);
        logger.removeHandler(handler);
    }

    @Test
    public void testLogSensitivePublicRuns() {
        logSensitivePublic();
    }
}
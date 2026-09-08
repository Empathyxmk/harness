package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.logging.Logger;

public class LoggerTest {
    @Test
    public void testLoggerImportable() {
        Logger logger = Logger.getLogger("claude_to_chatgpt");
        assertNotNull(logger);
        assertTrue(logger instanceof Logger);
    }
}
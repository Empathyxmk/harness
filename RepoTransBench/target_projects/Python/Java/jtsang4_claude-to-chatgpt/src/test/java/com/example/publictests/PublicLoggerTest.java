package com.example.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.logging.Level;
import java.util.logging.Logger;

public class PublicLoggerTest {

    @Test
    public void testPublicGetLoggerLevel() {
        Logger logger = Logger.getLogger("publicLoggerTest");
        assertTrue(logger instanceof Logger);
        logger.setLevel(Level.SEVERE);
        assertTrue(logger.getLevel() == Level.SEVERE || logger.getEffectiveLevel() == Level.SEVERE);
    }

    @Test
    public void testPublicGetLoggerName() {
        String loggerName = "unique_logger_name";
        Logger logger = Logger.getLogger(loggerName);
        assertEquals(loggerName, logger.getName());
    }
}
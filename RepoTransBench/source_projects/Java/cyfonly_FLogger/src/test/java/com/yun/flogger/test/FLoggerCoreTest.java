package com.yun.flogger.test;

import com.cyfonly.flogger.FLogger;
import com.cyfonly.flogger.constants.Constant;
import org.junit.Test;

public class FLoggerCoreTest {

    @Test
    public void testDebugInfoWarnErrorFatal() {
        FLogger logger = FLogger.getInstance();
        logger.debug("debug test message");
        logger.info("info test message");
        logger.warn("warn test message");
        logger.error("error test message");
        logger.fatal("fatal test message");
    }

    @Test
    public void testWriteLogWithLevel() {
        FLogger logger = FLogger.getInstance();
        logger.writeLog(Constant.DEBUG, "level debug");
        logger.writeLog(Constant.INFO, "level info");
        logger.writeLog(Constant.WARN, "level warn");
        logger.writeLog(Constant.ERROR, "level error");
        logger.writeLog(Constant.FATAL, "level fatal");
    }

    @Test
    public void testWriteLogNullAndBelowLevel() {
        FLogger logger = FLogger.getInstance();
        logger.writeLog("testfile", Constant.DEBUG, null); // null should not throw
        // Emulate level not in CFG_LOG_LEVEL
        String oldLevel = Constant.CFG_LOG_LEVEL;
        Constant.CFG_LOG_LEVEL = ""; // disable all
        logger.writeLog("shouldSkip", Constant.DEBUG, "skip this");
        Constant.CFG_LOG_LEVEL = oldLevel;
    }
}
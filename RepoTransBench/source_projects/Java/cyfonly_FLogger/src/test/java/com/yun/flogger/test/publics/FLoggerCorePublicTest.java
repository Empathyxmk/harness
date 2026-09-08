package com.yun.flogger.test.publics;

import com.cyfonly.flogger.FLogger;
import org.junit.Test;

public class FLoggerCorePublicTest {

    @Test
    public void testVariousLevelsPublic() {
        FLogger logger = FLogger.getInstance();
        // Use different messages and levels compared to original, including more threads
        logger.debug("Debugging - public core test!");
        logger.fatal("This is a public fatal log!");
        logger.writeLog("public_logfile", 2, "This is a public WARN log in a special file!");
    }
}
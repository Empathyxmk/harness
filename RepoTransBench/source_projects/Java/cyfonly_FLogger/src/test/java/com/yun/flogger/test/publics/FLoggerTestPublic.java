package com.yun.flogger.test.publics;

import com.cyfonly.flogger.FLogger;
import org.junit.Test;

public class FLoggerTestPublic {

    @Test
    public void testLoggerInfoAndWarnPublic() {
        FLogger logger = FLogger.getInstance();
        logger.info("Public INFO message for FLoggerTestPublic");
        logger.warn("Public WARN message for FLoggerTestPublic");
    }
}
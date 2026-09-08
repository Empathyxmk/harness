package com.yun.flogger.test.publics;

import com.cyfonly.flogger.strategy.LogManager;
import org.junit.Test;

import static org.junit.Assert.*;

public class LogManagerPublicTest {

    @Test
    public void testSingletonAndClosePublic() {
        LogManager logManager1 = LogManager.getInstance();
        LogManager logManager2 = LogManager.getInstance();
        assertSame(logManager1, logManager2);

        // Just call close to make sure no exception (cannot assert file contents)
        logManager1.close();
        // No assertion needed, just ensuring no exception thrown
    }
}
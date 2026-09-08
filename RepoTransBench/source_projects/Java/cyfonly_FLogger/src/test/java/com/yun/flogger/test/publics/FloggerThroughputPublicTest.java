package com.yun.flogger.test.publics;

import com.cyfonly.flogger.FLogger;
import org.junit.Test;

public class FloggerThroughputPublicTest {

    @Test
    public void publicThroughputDifferentLoop() {
        FLogger logger = FLogger.getInstance();
        // Use a non-1000 loop, different string
        int cnt = 10;
        for (int i = 0; i < cnt; i++) {
            logger.info("Public throughput message #" + i);
        }
    }
}
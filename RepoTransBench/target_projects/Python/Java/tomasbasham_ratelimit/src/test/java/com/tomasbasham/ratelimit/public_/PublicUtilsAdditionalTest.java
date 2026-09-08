package com.tomasbasham.ratelimit.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.tomasbasham.ratelimit.utils.Utils;

public class PublicUtilsAdditionalTest {

    @Test
    void testPublicNowMonotonicity() throws InterruptedException {
        double t1 = Utils.now().get();
        Thread.sleep(10);
        double t2 = Utils.now().get();
        assertTrue(t2 >= t1);
    }

    @Test
    void testPublicNowCloseToTimeTime() {
        double t1 = Utils.now().get();
        double t2 = System.currentTimeMillis() / 1000.0;
        assertTrue(Math.abs(t2 - t1) < 1.0);
    }
}
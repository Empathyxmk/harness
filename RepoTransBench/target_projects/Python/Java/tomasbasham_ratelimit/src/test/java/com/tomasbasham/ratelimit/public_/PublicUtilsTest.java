package com.tomasbasham.ratelimit.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.tomasbasham.ratelimit.utils.Utils;

public class PublicUtilsTest {

    @Test
    void testPublicNowTypeAndIncreasing() throws InterruptedException {
        double t1 = Utils.now().get();
        Thread.sleep(5);
        double t2 = Utils.now().get();
        assertTrue(t1 instanceof Double);
        assertTrue(t2 >= t1);
    }

    @Test
    void testPublicNowMonotonic() {
        double[] vals = {Utils.now().get(),
                         Utils.now().get(),
                         Utils.now().get()};
        assertTrue(vals[1] >= vals[0]);
        assertTrue(vals[2] >= vals[1]);
    }
}
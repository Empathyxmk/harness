package org.LatencyUtils;

import org.junit.Test;

public class TimeServicesTest {

    @Test
    public void testNanoTimeAndMillisStatic() {
        long n1 = TimeServices.nanoTime();
        long m1 = TimeServices.currentTimeMillis();
        assert n1 > 0;
        assert m1 > 0;
    }
}
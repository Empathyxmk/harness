package com.github.nexmark.flink.metric;

import com.github.nexmark.flink.metric.tps.TpsMetric;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TpsMetricPublicTest {

    @Test
    void testTpsMetricSettersGetters() {
        TpsMetric metric = new TpsMetric();
        metric.setStartTime(22222L);
        metric.setEndTime(33333L);
        metric.setTps(12345.6);
        metric.setNum(77L);

        assertEquals(22222L, metric.getStartTime());
        assertEquals(33333L, metric.getEndTime());
        assertEquals(12345.6, metric.getTps());
        assertEquals(77L, metric.getNum());
    }
}
package com.github.nexmark.flink.metric;

import com.github.nexmark.flink.metric.cpu.CpuMetric;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class CpuMetricPublicTest {

    @Test
    void testCpuMetricDifferentValues() {
        CpuMetric metric = new CpuMetric(234.56, 1900L, 14.7f, 100.2, "nodeX");
        assertEquals(234.56, metric.getProcessCpuTimeSeconds());
        assertEquals(1900L, metric.getProcessTotalCpuMilliseconds());
        assertEquals(14.7f, metric.getProcessCpuLoad());
        assertEquals(100.2, metric.getSystemCpuLoad());
        assertEquals("nodeX", metric.getHostName());
    }

    @Test
    void testToStringNotEmpty() {
        CpuMetric metric = new CpuMetric(0.99, 99L, 2.2f, 88.1, "hostY");
        String s = metric.toString();
        assertTrue(s.contains("hostY"));
        assertTrue(s.length() > 0);
    }
}
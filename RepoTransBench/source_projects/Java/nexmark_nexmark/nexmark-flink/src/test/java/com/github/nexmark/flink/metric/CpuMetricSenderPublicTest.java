package com.github.nexmark.flink.metric;

import com.github.nexmark.flink.metric.cpu.CpuMetricSender;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class CpuMetricSenderPublicTest {

    @Test
    void testMetricSenderHostAndPort() {
        // Different host and port than original
        CpuMetricSender sender = new CpuMetricSender("testhost", 10000);
        assertEquals("testhost", sender.getHost());
        assertEquals(10000, sender.getPort());
    }

    @Test
    void testMetricSenderNegativePort() {
        CpuMetricSender sender = new CpuMetricSender("anotherhost", -1);
        assertEquals(-1, sender.getPort());
    }
}
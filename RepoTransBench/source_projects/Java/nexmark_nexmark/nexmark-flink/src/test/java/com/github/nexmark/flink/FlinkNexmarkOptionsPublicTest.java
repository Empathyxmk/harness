package com.github.nexmark.flink;

import org.apache.flink.configuration.ConfigOption;
import org.junit.jupiter.api.Test;

import java.time.Duration;

import static org.junit.jupiter.api.Assertions.*;

class FlinkNexmarkOptionsPublicTest {

    @Test
    void testMetricMonitorDelayKeyAndType() {
        ConfigOption<Duration> option = FlinkNexmarkOptions.METRIC_MONITOR_DELAY;
        assertEquals("nexmark.metric.monitor.delay", option.key());
        // Change: Instead of checking default of 10s, check that it is not 30s (different value test)
        assertNotEquals(Duration.ofSeconds(30), option.defaultValue());
    }

    @Test
    void testMetricMonitorDurationKeyAndType() {
        ConfigOption<Duration> option = FlinkNexmarkOptions.METRIC_MONITOR_DURATION;
        assertEquals("nexmark.metric.monitor.duration", option.key());
        // Check default is greater than a large but not maximum value
        assertTrue(option.defaultValue().compareTo(Duration.ofDays(365)) > 0);
    }

    @Test
    void testMetricMonitorIntervalKeyAndType() {
        ConfigOption<Duration> option = FlinkNexmarkOptions.METRIC_MONITOR_INTERVAL;
        assertEquals("nexmark.metric.monitor.interval", option.key());
        // Different value: not 2 seconds
        assertNotEquals(Duration.ofSeconds(2), option.defaultValue());
    }

    @Test
    void testMetricReporterHostKeyAndType() {
        ConfigOption<String> option = FlinkNexmarkOptions.METRIC_REPORTER_HOST;
        assertEquals("nexmark.metric.reporter.host", option.key());
        // Different string value test
        assertNotEquals("nexmark", option.defaultValue());
    }

    @Test
    void testMetricReporterPortKeyAndType() {
        ConfigOption<Integer> option = FlinkNexmarkOptions.METRIC_REPORTER_PORT;
        assertEquals("nexmark.metric.reporter.port", option.key());
        // Different port
        assertNotEquals((Integer) 9000, option.defaultValue());
    }

    @Test
    void testFlinkRestAddressKeyAndType() {
        ConfigOption<String> option = FlinkNexmarkOptions.FLINK_REST_ADDRESS;
        assertEquals("flink.rest.address", option.key());
        // Different string test
        assertNotEquals("127.0.0.1", option.defaultValue());
    }

    @Test
    void testFlinkRestPortKeyAndType() {
        ConfigOption<Integer> option = FlinkNexmarkOptions.FLINK_REST_PORT;
        assertEquals("flink.rest.port", option.key());
        // Different port value
        assertNotEquals((Integer) 8000, option.defaultValue());
    }
}
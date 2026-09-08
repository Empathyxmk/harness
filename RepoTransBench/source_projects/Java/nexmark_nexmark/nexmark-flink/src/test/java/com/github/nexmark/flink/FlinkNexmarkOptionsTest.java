package com.github.nexmark.flink;

import org.apache.flink.configuration.ConfigOption;
import org.junit.jupiter.api.Test;

import java.time.Duration;

import static org.junit.jupiter.api.Assertions.*;

class FlinkNexmarkOptionsTest {

    @Test
    void testMetricMonitorDelayDefaults() {
        ConfigOption<Duration> option = FlinkNexmarkOptions.METRIC_MONITOR_DELAY;
        assertEquals("nexmark.metric.monitor.delay", option.key());
        assertEquals(Duration.ofSeconds(10), option.defaultValue());
    }

    @Test
    void testMetricMonitorDurationDefaults() {
        ConfigOption<Duration> option = FlinkNexmarkOptions.METRIC_MONITOR_DURATION;
        assertEquals("nexmark.metric.monitor.duration", option.key());
        assertEquals(Duration.ofNanos(Long.MAX_VALUE), option.defaultValue());
    }

    @Test
    void testMetricMonitorIntervalDefaults() {
        ConfigOption<Duration> option = FlinkNexmarkOptions.METRIC_MONITOR_INTERVAL;
        assertEquals("nexmark.metric.monitor.interval", option.key());
        assertEquals(Duration.ofSeconds(5), option.defaultValue());
    }

    @Test
    void testMetricReporterHostDefaults() {
        ConfigOption<String> option = FlinkNexmarkOptions.METRIC_REPORTER_HOST;
        assertEquals("nexmark.metric.reporter.host", option.key());
        assertEquals("localhost", option.defaultValue());
    }

    @Test
    void testMetricReporterPortDefaults() {
        ConfigOption<Integer> option = FlinkNexmarkOptions.METRIC_REPORTER_PORT;
        assertEquals("nexmark.metric.reporter.port", option.key());
        assertEquals((Integer) 9098, option.defaultValue());
    }

    @Test
    void testFlinkRestAddressDefaults() {
        ConfigOption<String> option = FlinkNexmarkOptions.FLINK_REST_ADDRESS;
        assertEquals("flink.rest.address", option.key());
        assertEquals("localhost", option.defaultValue());
    }

    @Test
    void testFlinkRestPortDefaults() {
        ConfigOption<Integer> option = FlinkNexmarkOptions.FLINK_REST_PORT;
        assertEquals("flink.rest.port", option.key());
        assertEquals((Integer) 8081, option.defaultValue());
    }
}
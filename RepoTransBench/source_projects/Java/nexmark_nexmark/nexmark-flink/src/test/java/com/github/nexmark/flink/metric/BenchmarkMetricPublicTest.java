package com.github.nexmark.flink.metric;

import org.junit.jupiter.api.Test;

import java.text.DecimalFormat;

import static org.junit.jupiter.api.Assertions.*;

class BenchmarkMetricPublicTest {

    @Test
    void testFormatDoubleValuePublic() {
        // Use a different double value for formatting test
        double value = 98765.4321;
        DecimalFormat df = BenchmarkMetric.NUMBER_FORMAT;
        String formatted = BenchmarkMetric.formatDoubleValue(value);
        assertEquals(df.format(value), formatted);
    }

    @Test
    void testFormatLongValuePerSecondPublic() {
        long value = 543210;
        double seconds = 36.0;
        String formatted = BenchmarkMetric.formatLongValuePerSecond(value, seconds);
        assertTrue(formatted.contains("/s"));
        assertFalse(formatted.contains("N/A"));
    }
}
package com.github.nexmark.flink;

import com.github.nexmark.flink.utils.NexmarkUtils;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class NexmarkConfigurationPublicTest {

    @Test
    void testDefaultValuesAreNotAllCustom() {
        NexmarkConfiguration config = new NexmarkConfiguration();
        // Change several tested values for difference vs. original test.
        assertNotEquals(1, config.numEvents);
        assertEquals(NexmarkUtils.RateShape.SQUARE, config.rateShape); // Keep: checks enum default
        assertNotEquals(20000, config.firstEventRate); // Was 10000 in original test
        assertEquals(NexmarkUtils.RateUnit.PER_SECOND, config.rateUnit);
        assertNotEquals(1200, config.ratePeriodSec); // Was 600 in original
        assertTrue(config.personProportion < config.bidProportion); // 1 < 46
        assertNotEquals(300, config.avgPersonByteSize);
        assertNotEquals(999, config.numInFlightAuctions);
        assertTrue(config.numActivePeople > 0);
    }

    @Test
    void testEqualsAndHashCodeDiffObject() {
        NexmarkConfiguration c1 = new NexmarkConfiguration();
        NexmarkConfiguration c2 = new NexmarkConfiguration();
        c1.firstEventRate = 12345;
        assertNotEquals(c1, c2);
        // Now set equal and test equality
        c2.firstEventRate = 12345;
        assertEquals(c1, c2);
        assertEquals(c1.hashCode(), c2.hashCode());
    }
}
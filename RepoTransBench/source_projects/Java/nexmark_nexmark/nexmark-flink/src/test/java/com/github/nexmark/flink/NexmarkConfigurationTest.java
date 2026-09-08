package com.github.nexmark.flink;

import com.github.nexmark.flink.utils.NexmarkUtils;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class NexmarkConfigurationTest {

    @Test
    void testDefaultValues() {
        NexmarkConfiguration config = new NexmarkConfiguration();
        assertEquals(0, config.numEvents);
        assertEquals(1, config.numEventGenerators);
        assertEquals(NexmarkUtils.RateShape.SQUARE, config.rateShape);
        assertEquals(10000, config.firstEventRate);
        assertEquals(10000, config.nextEventRate);
        assertEquals(NexmarkUtils.RateUnit.PER_SECOND, config.rateUnit);
        assertEquals(600, config.ratePeriodSec);
        assertEquals(0, config.preloadSeconds);
        assertEquals(240, config.streamTimeout);
        assertFalse(config.isRateLimited);
        assertFalse(config.useWallclockEventTime);
        assertEquals(1, config.personProportion);
        assertEquals(3, config.auctionProportion);
        assertEquals(46, config.bidProportion);
        assertEquals(200, config.avgPersonByteSize);
        assertEquals(500, config.avgAuctionByteSize);
        assertEquals(100, config.avgBidByteSize);
        assertEquals(2, config.hotAuctionRatio);
        assertEquals(4, config.hotSellersRatio);
        assertEquals(4, config.hotBiddersRatio);
        assertEquals(10, config.windowSizeSec);
        assertEquals(5, config.windowPeriodSec);
        assertEquals(0, config.watermarkHoldbackSec);
        assertEquals(100, config.numInFlightAuctions);
        assertEquals(1000, config.numActivePeople);
    }

    @Test
    void testEqualsAndHashCode() {
        NexmarkConfiguration c1 = new NexmarkConfiguration();
        NexmarkConfiguration c2 = new NexmarkConfiguration();
        assertEquals(c1, c2);
        assertEquals(c1.hashCode(), c2.hashCode());
        c2.numEvents = 100;
        assertNotEquals(c1, c2);
    }
}
package com.github.nexmark.flink.generator;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class NexmarkGeneratorPublicTest {

    @Test
    void testInitialEventGeneration() {
        NexmarkGenerator generator = new NexmarkGenerator(250L, 1, 500L, 3, 99);
        assertNotNull(generator.nextEvent());
        assertEquals(1, generator.getMaxPersonId()); // Confirm part of config used in event
    }

    @Test
    void testBidSequenceGenerated() {
        NexmarkGenerator generator = new NexmarkGenerator(20L, 2, 100L, 2, 66);
        for (int i = 0; i < 5; i++) {
            assertNotNull(generator.nextEvent());
        }
        assertTrue(generator.getMaxAuctionId() > 0);
    }
}
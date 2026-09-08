package com.github.nexmark.flink.source;

import org.apache.flink.table.factories.TableFactory;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class NexmarkTableSourceFactoryPublicTest {

    @Test
    void testFactoryClassType() {
        TableFactory factory = new NexmarkTableSourceFactory();
        assertTrue(factory instanceof NexmarkTableSourceFactory);
    }

    @Test
    void testFactoryToStringNotNull() {
        TableFactory factory = new NexmarkTableSourceFactory();
        assertNotNull(factory.toString());
    }
}
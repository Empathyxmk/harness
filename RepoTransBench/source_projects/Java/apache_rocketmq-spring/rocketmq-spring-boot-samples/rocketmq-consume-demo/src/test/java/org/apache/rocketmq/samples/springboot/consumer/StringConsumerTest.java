package org.apache.rocketmq.samples.springboot.consumer;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class StringConsumerTest {

    @Test
    void testOnMessage() {
        StringConsumer consumer = new StringConsumer();
        // Should not throw exceptions and print output
        assertDoesNotThrow(() -> consumer.onMessage("hello test"));
    }
}
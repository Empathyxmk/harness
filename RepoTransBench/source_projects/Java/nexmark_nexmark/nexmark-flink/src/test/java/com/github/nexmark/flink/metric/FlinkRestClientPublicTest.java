package com.github.nexmark.flink.metric;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class FlinkRestClientPublicTest {

    @Test
    void testAddressWithPort() {
        FlinkRestClient client = new FlinkRestClient("192.168.0.100", 9000);
        assertEquals("192.168.0.100", client.getRestAddress());
        assertEquals(9000, client.getRestPort());
    }

    @Test
    void testRestAddressNotDefault() {
        FlinkRestClient client = new FlinkRestClient("example.com", 12345);
        assertNotEquals("localhost", client.getRestAddress());
        assertEquals(12345, client.getRestPort());
    }
}
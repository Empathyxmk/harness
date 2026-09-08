package com.example.environ.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestChannels {

    @Test
    void testDefaultChannelConfig() {
        ChannelConfig config = ChannelConfig.defaultChannel();
        assertEquals("inmemory", config.getBackend());
    }

    @Test
    void testParseChannelConfig() {
        ChannelConfig config = ChannelConfig.fromUrl("redis://localhost:6379");
        assertEquals("redis", config.getBackend());
        assertEquals("localhost:6379", config.getLocation());
    }
}
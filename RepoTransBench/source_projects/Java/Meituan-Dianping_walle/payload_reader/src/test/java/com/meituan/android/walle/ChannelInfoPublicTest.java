package com.meituan.android.walle;

import org.junit.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.Assert.*;

public class ChannelInfoPublicTest {

    @Test
    public void testGettersAndToString_public() {
        Map<String, String> info = new HashMap<>();
        info.put("testKey", "testVal");
        ChannelInfo channelInfo = new ChannelInfo("pub-channel", info);

        assertEquals("pub-channel", channelInfo.getChannel());
        assertEquals("testVal", channelInfo.getExtraInfo().get("testKey"));
        assertTrue(channelInfo.toString().contains("pub-channel"));
        assertTrue(channelInfo.toString().contains("testKey"));
        assertTrue(channelInfo.toString().contains("testVal"));
    }

    @Test
    public void testNullExtraInfo_public() {
        ChannelInfo channelInfo = new ChannelInfo("pub-label", null);
        assertEquals("pub-label", channelInfo.getChannel());
        assertNull(channelInfo.getExtraInfo());
        assertTrue(channelInfo.toString().contains("pub-label"));
        assertTrue(channelInfo.toString().contains("null"));
    }
}
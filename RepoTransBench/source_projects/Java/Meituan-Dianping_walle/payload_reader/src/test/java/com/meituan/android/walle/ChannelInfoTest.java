package com.meituan.android.walle;

import org.junit.Test;
import java.util.HashMap;
import java.util.Map;

import static org.junit.Assert.*;

public class ChannelInfoTest {
    @Test
    public void testConstructorAndGetters_basic() {
        Map<String, String> extra = new HashMap<>();
        extra.put("k1", "v1");
        ChannelInfo info = new ChannelInfo("channelA", extra);
        assertEquals("channelA", info.getChannel());
        assertEquals(extra, info.getExtraInfo());
    }

    @Test
    public void testConstructorAndGetters_nullExtra() {
        ChannelInfo info = new ChannelInfo("abc", null);
        assertEquals("abc", info.getChannel());
        assertNull(info.getExtraInfo());
    }

    @Test
    public void testConstructorAndGetters_nullChannel() {
        Map<String, String> extra = new HashMap<>();
        ChannelInfo info = new ChannelInfo(null, extra);
        assertNull(info.getChannel());
        assertEquals(extra, info.getExtraInfo());
    }
}
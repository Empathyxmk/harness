package com.meituan.android.walle;

import org.junit.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.Assert.*;

public class ChannelInfoEqualsHashCodeTest {

    @Test
    public void testEqualsAndHashCode() {
        Map<String, String> extraA = new HashMap<>();
        extraA.put("foo", "bar");
        ChannelInfo a = new ChannelInfo("ch", extraA);
        ChannelInfo b = new ChannelInfo("ch", extraA);
        assertEquals(a, b);
        assertEquals(a.hashCode(), b.hashCode());

        // different channel
        ChannelInfo c = new ChannelInfo("c2", extraA);
        assertNotEquals(a, c);

        // different extraInfo
        ChannelInfo d = new ChannelInfo("ch", null);
        assertNotEquals(a, d);

        // null channel
        ChannelInfo e = new ChannelInfo(null, extraA);
        ChannelInfo f = new ChannelInfo(null, extraA);
        assertEquals(e, f);
        assertEquals(e.hashCode(), f.hashCode());
    }
}
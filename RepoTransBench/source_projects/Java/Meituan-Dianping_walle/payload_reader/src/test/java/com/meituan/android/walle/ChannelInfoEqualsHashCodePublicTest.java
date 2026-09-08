package com.meituan.android.walle;

import org.junit.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.Assert.*;

public class ChannelInfoEqualsHashCodePublicTest {

    @Test
    public void testEqualsAndHashCode_public() {
        Map<String, String> extraA = new HashMap<>();
        extraA.put("baz", "qux");
        ChannelInfo a = new ChannelInfo("public", extraA);
        ChannelInfo b = new ChannelInfo("public", extraA);
        assertEquals(a, b);
        assertEquals(a.hashCode(), b.hashCode());

        // different channel
        ChannelInfo c = new ChannelInfo("diff", extraA);
        assertNotEquals(a, c);

        // different extraInfo
        ChannelInfo d = new ChannelInfo("public", null);
        assertNotEquals(a, d);

        // null channel
        ChannelInfo e = new ChannelInfo(null, extraA);
        ChannelInfo f = new ChannelInfo(null, extraA);
        assertEquals(e, f);
        assertEquals(e.hashCode(), f.hashCode());
    }
}
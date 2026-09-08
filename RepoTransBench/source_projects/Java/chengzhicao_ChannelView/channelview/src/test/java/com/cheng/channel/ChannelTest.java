package com.cheng.channel;

import org.junit.Test;
import static org.junit.Assert.*;

public class ChannelTest {
    @Test
    public void testChannel_ConstructorsAndGetters() {
        Channel c1 = new Channel("News");
        assertEquals("News", c1.getChannelName());

        Channel c2 = new Channel("Fun", 2, "extra");
        assertEquals("Fun", c2.getChannelName());
        assertEquals("extra", c2.getObj());

        Channel c3 = new Channel("Sports", 3);
        assertEquals("Sports", c3.getChannelName());

        Channel c4 = new Channel("Games", "objval");
        assertEquals("Games", c4.getChannelName());
        assertEquals("objval", c4.getObj());
    }

    @Test
    public void testChannel_Setters() {
        Channel c = new Channel("Initial");
        c.setChannelName("Changed");
        c.setObj(1001);
        assertEquals("Changed", c.getChannelName());
        assertEquals(1001, c.getObj());
    }

    @Test
    public void testChannel_ToString() {
        Channel c = new Channel("Stringy", "val");
        String s = c.toString();
        assertTrue(s.contains("channelName='Stringy'"));
        assertTrue(s.contains("obj=val"));
    }
}
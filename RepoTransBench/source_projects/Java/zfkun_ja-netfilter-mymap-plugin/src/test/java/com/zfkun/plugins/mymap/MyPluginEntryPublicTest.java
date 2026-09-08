package com.zfkun.plugins.mymap;

import com.janetfilter.core.plugin.PluginConfig;
import org.junit.Test;

import static org.junit.Assert.*;

public class MyPluginEntryPublicTest {

    @Test
    public void testInitAndGetters_public() {
        MyPluginEntry entry = new MyPluginEntry();
        entry.init(null, new PluginConfig());
        assertNotNull(entry.getTransformers());
    }

    @Test
    public void testMeta_public() {
        MyPluginEntry entry = new MyPluginEntry();
        assertEquals("MyMapPlugin", entry.getName());
        assertEquals("zfkun", entry.getAuthor());
        assertEquals("1.0.0", entry.getVersion());
        assertTrue(entry.getDescription().toLowerCase().contains("plugin"));
    }
}
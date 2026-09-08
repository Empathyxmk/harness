package com.meituan.android.walle;

import org.json.JSONException;
import org.junit.Test;

import java.io.File;
import java.util.HashMap;
import java.util.Map;

import static org.junit.Assert.*;

public class ChannelReaderTest {

    @Test
    public void testGetChannel_normal() throws Exception {
        // Prepare a fake channel info
        File file = null;
        // ChannelReader returns null for null files
        assertNull(ChannelReader.getChannel(file));
    }

    @Test
    public void testGetChannelInfo_normal() throws Exception {
        File file = null;
        assertNull(ChannelReader.getChannelInfo(file));
    }

    @Test
    public void testGetChannelInfoMap_nullFile() throws Exception {
        File file = null;
        assertNull(ChannelReader.getChannelInfoMap(file));
    }

    @Test
    public void testParseChannel_nullString() {
        assertNull(ChannelReader.parseChannel(null));
    }

    @Test
    public void testParseChannel_malformed() {
        // Malformed JSON string
        String malformed = "{not-a-json}";
        assertNull(ChannelReader.parseChannel(malformed));
    }

    @Test
    public void testParseChannel_valid() {
        String json = "{\"channel\":\"TestChannel\",\"extra\":{\"foo\":\"bar\"}}";
        ChannelInfo info = ChannelReader.parseChannel(json);
        assertNotNull(info);
        assertEquals("TestChannel", info.getChannel());
        assertNotNull(info.getExtraInfo());
        assertEquals("bar", info.getExtraInfo().get("foo"));
    }

    @Test
    public void testParseChannel_valid_noExtra() {
        String json = "{\"channel\":\"A\"}";
        ChannelInfo info = ChannelReader.parseChannel(json);
        assertNotNull(info);
        assertEquals("A", info.getChannel());
        assertNull(info.getExtraInfo());
    }

    @Test
    public void testParseChannel_valid_nullChannel() {
        String json = "{\"extra\":{\"foo\":\"bar\"}}";
        ChannelInfo info = ChannelReader.parseChannel(json);
        assertNotNull(info);
        assertNull(info.getChannel());
        assertNotNull(info.getExtraInfo());
        assertEquals("bar", info.getExtraInfo().get("foo"));
    }
}
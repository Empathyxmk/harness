package net.yacy.grid.crawler.api;

import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class CrawlStartServicePublicTest {

    @Test
    public void testParseTimeout_Public() {
        // Use different parameters than in the original: 90 instead of 30, 250 instead of 150
        Map<String, String[]> params = new HashMap<>();
        params.put("timeout", new String[]{"90"});
        int result = CrawlStartService.parseTimeout(params, 250);
        assertEquals(90, result);
    }

    @Test
    public void testParseTimeout_Defaults_Public() {
        // No timeout param should use default, so let's use 60 instead of 120
        Map<String, String[]> params = new HashMap<>();
        int result = CrawlStartService.parseTimeout(params, 60);
        assertEquals(60, result);
    }

    @Test
    public void testParseTimeout_Invalid_Public() {
        // timeout present but not a number
        Map<String, String[]> params = new HashMap<>();
        params.put("timeout", new String[]{"invalid"});
        int result = CrawlStartService.parseTimeout(params, 15);
        assertEquals(15, result);
    }
}
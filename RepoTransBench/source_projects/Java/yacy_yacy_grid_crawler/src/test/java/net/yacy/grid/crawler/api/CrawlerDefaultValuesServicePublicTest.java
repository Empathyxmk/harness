package net.yacy.grid.crawler.api;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class CrawlerDefaultValuesServicePublicTest {

    @Test
    public void testGetDefaultTimeout_Public() {
        // Just make sure the default timeout routine returns the value
        int defaultTimeout = CrawlerDefaultValuesService.getDefaultTimeout();
        // In public test, just assert it is a positive value
        assertTrue(defaultTimeout > 0);
    }

    @Test
    public void testDefaultValuesConstants_Public() {
        // Use different logic: verify that defaultMaxDepth and defaultMaxLinks are positive and not zero
        int depth = CrawlerDefaultValuesService.defaultMaxDepth;
        int links = CrawlerDefaultValuesService.defaultMaxLinks;
        assertTrue(depth > 0 && links > 0);
        assertTrue(depth != 0 && links != 0);
    }
}
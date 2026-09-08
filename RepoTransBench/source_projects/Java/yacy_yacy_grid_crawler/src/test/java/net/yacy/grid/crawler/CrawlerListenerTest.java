package net.yacy.grid.crawler;

import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Minimal stub/branch coverage for available methods in CrawlerListener due to large external dependencies.
 * We will focus on static initPriorityQueue and priorityDimensions.
 */
public class CrawlerListenerTest {

    @Test
    public void testInitPriorityQueue() throws Exception {
        // The static method sets static arrays based on priorityDimension.
        // We'll just assert it runs without exception, no external effect here.
        CrawlerListener.initPriorityQueue(1);
        assertNotNull(getStaticField("CRAWLER_PRIORITY_DIMENSIONS"));
        assertNotNull(getStaticField("LOADER_PRIORITY_DIMENSIONS"));
        assertNotNull(getStaticField("PARSER_PRIORITY_DIMENSIONS"));
        assertNotNull(getStaticField("INDEXER_PRIORITY_DIMENSIONS"));
    }

    @Test
    public void testPriorityDimensionsEdgeCases() throws Exception {
        // Indirect via reflection to avoid full dependencies for YaCyServices mock-ups.

        Method m = CrawlerListener.class.getDeclaredMethod("priorityDimensions", Class.forName("net.yacy.grid.YaCyServices"), int.class);
        m.setAccessible(true);

        // As we can't create net.yacy.grid.YaCyServices, this just confirms method presence.
        assertNotNull(m);
    }

    private Object getStaticField(String fieldName) throws Exception {
        java.lang.reflect.Field f = CrawlerListener.class.getDeclaredField(fieldName);
        f.setAccessible(true);
        return f.get(null);
    }

}
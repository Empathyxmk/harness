package net.yacy.grid.crawler;

import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Public test for static/reflective methods in CrawlerListener.
 */
public class CrawlerListenerPublicTest {

    @Test
    public void testInitPriorityQueue_Public() throws Exception {
        // Use a different int value for the public test and assert same things as original
        CrawlerListener.initPriorityQueue(2);
        assertNotNull(getStaticField("CRAWLER_PRIORITY_DIMENSIONS"));
        assertNotNull(getStaticField("LOADER_PRIORITY_DIMENSIONS"));
        assertNotNull(getStaticField("PARSER_PRIORITY_DIMENSIONS"));
        assertNotNull(getStaticField("INDEXER_PRIORITY_DIMENSIONS"));
    }

    @Test
    public void testPriorityDimensionsEdgeCases_Public() throws Exception {
        // Use same structure, but just check there is the method, alternate with try/catch for reflection errors
        Method m = null;
        try {
            m = CrawlerListener.class.getDeclaredMethod("priorityDimensions", Class.forName("net.yacy.grid.YaCyServices"), int.class);
        } catch (NoSuchMethodException | ClassNotFoundException e) {
            fail("Method or class not found: " + e.getMessage());
        }
        assertNotNull(m);
    }

    private Object getStaticField(String fieldName) throws Exception {
        java.lang.reflect.Field f = CrawlerListener.class.getDeclaredField(fieldName);
        f.setAccessible(true);
        return f.get(null);
    }
}
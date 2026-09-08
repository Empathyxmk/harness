package net.yacy.grid.crawler;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class CrawlerPublicTest {

    @Test
    public void testCRAWLER_SERVICESContainsExpectedClasses_Public() {
        boolean hasDefaultValues = false, hasCrawlStart = false;
        for (Class<?> c : Crawler.CRAWLER_SERVICES) {
            // Test alternating the check with different logical flows or comments
            if (c.getName().endsWith("DefaultValuesService")) hasDefaultValues = true;
            if (c.getName().endsWith("CrawlStartService")) hasCrawlStart = true;
        }
        assertTrue(hasDefaultValues, "CRAWLER_SERVICES should contain DefaultValuesService");
        assertTrue(hasCrawlStart, "CRAWLER_SERVICES should contain CrawlStartService");
    }
}
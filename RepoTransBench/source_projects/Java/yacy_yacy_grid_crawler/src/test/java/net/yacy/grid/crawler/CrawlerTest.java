package net.yacy.grid.crawler;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class CrawlerTest {

    @Test
    public void testCRAWLER_SERVICESContainsExpectedClasses() {
        boolean hasDefaultValues = false, hasCrawlStart = false;
        for (Class<?> c : Crawler.CRAWLER_SERVICES) {
            if (c.getSimpleName().equals("CrawlerDefaultValuesService")) hasDefaultValues = true;
            if (c.getSimpleName().equals("CrawlStartService")) hasCrawlStart = true;
        }
        assertTrue(hasDefaultValues, "CRAWLER_SERVICES should contain CrawlerDefaultValuesService");
        assertTrue(hasCrawlStart, "CRAWLER_SERVICES should contain CrawlStartService");
    }
}
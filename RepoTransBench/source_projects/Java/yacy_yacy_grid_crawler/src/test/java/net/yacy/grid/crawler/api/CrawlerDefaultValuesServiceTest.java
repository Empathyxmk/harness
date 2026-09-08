package net.yacy.grid.crawler.api;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import net.yacy.grid.http.Query;
import net.yacy.grid.http.ServiceResponse;

import static org.junit.jupiter.api.Assertions.*;

public class CrawlerDefaultValuesServiceTest {

    @Test
    public void testGetAPIPath() {
        CrawlerDefaultValuesService service = new CrawlerDefaultValuesService();
        assertTrue(service.getAPIPath().endsWith("/defaultValues.json"));
    }

    @Test
    public void testCrawlStartDefaultClone() {
        JSONObject original = CrawlerDefaultValuesService.defaultValues;
        JSONObject clone = CrawlerDefaultValuesService.crawlStartDefaultClone();
        for (String key : original.keySet()) {
            assertEquals(original.get(key).toString(), clone.get(key).toString());
        }
        // Cloning should produce a different instance
        assertNotSame(original, clone);
    }

    @Test
    public void testServiceImplReturnsDefaultValues() {
        CrawlerDefaultValuesService service = new CrawlerDefaultValuesService();
        ServiceResponse resp = service.serviceImpl(new Query(null), null);
        assertNotNull(resp);
        JSONObject json = resp.toJSON();
        for (String key : CrawlerDefaultValuesService.defaultValues.keySet()) {
            assertEquals(CrawlerDefaultValuesService.defaultValues.get(key).toString(), json.get(key).toString());
        }
    }
}
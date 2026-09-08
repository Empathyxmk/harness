package net.yacy.grid.crawler.api;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import net.yacy.grid.http.Query;
import net.yacy.grid.http.ServiceResponse;

import static org.junit.jupiter.api.Assertions.*;

public class CrawlStartServiceTest {

    @Test
    public void testGetAPIPath() {
        CrawlStartService service = new CrawlStartService();
        assertTrue(service.getAPIPath().endsWith("/crawlStart.json"));
    }

    @Test
    public void testServiceImplReturnsMergedDefaults() {
        CrawlStartService service = new CrawlStartService();
        Query call = new Query(null);
        ServiceResponse resp = service.serviceImpl(call, null);
        assertNotNull(resp);
        JSONObject json = resp.toJSON();
        // Some key fields must exist
        assertTrue(json.has("crawlingDepth"), "Missing crawlingDepth");
        assertTrue(json.has("mustmatch"), "Missing mustmatch");
        assertTrue(json.has("user_id"), "Missing user_id");
        assertTrue(json.has("crawlingURL"), "Missing crawlingURL");
    }

    @Test
    public void testServiceImplWithOverride() {
        CrawlStartService service = new CrawlStartService();
        Query call = new Query(null);
        call.set("crawlingDepth", 10);
        call.set("user_id", "user42");
        ServiceResponse resp = service.serviceImpl(call, null);
        JSONObject json = resp.toJSON();
        // crawlingDepth shall not exceed 8
        assertEquals(8, json.getInt("crawlingDepth"));
        assertEquals("user42", json.getString("user_id"));
    }
}
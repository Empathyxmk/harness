package com.zaproxy.zaproxy.public_tests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
import java.util.Map;
import java.util.HashMap;

class FakeBrkModule {
    public Map<String, Object> add_break_point(String url, String method) {
        Map<String, Object> resp = new HashMap<>();
        resp.put("status", "OK");
        resp.put("method", method);
        resp.put("url", url);
        return resp;
    }
    public Map<String, Object> remove_break_point(String brkId) {
        Map<String, Object> resp = new HashMap<>();
        resp.put("status", "REMOVED");
        resp.put("id", brkId);
        return resp;
    }
}

public class PublicBrkTest {
    FakeBrkModule brk = new FakeBrkModule();

    @Test
    public void testBrkAddBreakPointDiffData() {
        String url = "http://public.example.com/login";
        String method = "POST";
        Map<String, Object> response = brk.add_break_point(url, method);
        assertEquals("OK", response.get("status"));
        assertEquals(method, response.get("method"));
        assertTrue(((String)response.get("url")).startsWith("http://public."));
    }

    @Test
    public void testBrkRemoveBreakPointDiffData() {
        String brkId = "customBrk2";
        Map<String, Object> response = brk.remove_break_point(brkId);
        assertEquals("REMOVED", response.get("status"));
        assertEquals(brkId, response.get("id"));
    }
}
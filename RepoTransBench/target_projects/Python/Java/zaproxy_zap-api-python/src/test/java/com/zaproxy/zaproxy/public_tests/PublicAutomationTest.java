package com.zaproxy.zaproxy.public_tests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
import java.util.Map;
import java.util.HashMap;

class FakeAutomationModule {
    public Map<String, Object> get_progress(int id) {
        Map<String, Object> map = new HashMap<>();
        map.put("progress", 10); // public data: progress != 0
        return map;
    }
}

public class PublicAutomationTest {
    private FakeAutomationModule automation = new FakeAutomationModule();

    @Test
    public void testGetProgressDifferentData() {
        int progress_id = 7;
        Map<String, Object> response = automation.get_progress(progress_id);
        assertTrue(response instanceof Map);
        assertTrue(response.containsKey("progress"));
        assertNotEquals(0, response.get("progress"));
    }
}
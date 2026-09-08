package com.zaproxy.zaproxy.public_tests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
import java.util.Map;
import java.util.HashMap;

class FakeRuleConfigModule {
    private Map<String, Map<String, Object>> store = new HashMap<>();
    public Map<String, Object> set_rule_config_value(String ruleId, String key, String value) {
        Map<String, Object> result = new HashMap<>();
        result.put("status", "UPDATED");
        result.put("ruleId", ruleId);
        Map<String, Object> inner = new HashMap<>();
        inner.put(key, value);
        store.put(ruleId, inner);
        return result;
    }
    public Map<String, Object> get_rule_config_value(String ruleId, String key) {
        Map<String, Object> out = new HashMap<>();
        if (store.containsKey(ruleId) && store.get(ruleId).containsKey(key)) {
            out.put("value", store.get(ruleId).get(key));
            out.put("key", key);
        } else {
            out.put("value", null);
            out.put("key", key);
        }
        return out;
    }
}

public class PublicRuleConfigTest {
    private FakeRuleConfigModule ruleConfig = new FakeRuleConfigModule();

    @Test
    public void testRuleConfigSetAndGetDiffData() {
        String ruleId = "12001";
        String key = "attackStrength";
        String value = "LOW";
        Map<String, Object> setResp = ruleConfig.set_rule_config_value(ruleId, key, value);
        assertEquals("UPDATED", setResp.get("status"));
        assertEquals(ruleId, setResp.get("ruleId"));

        Map<String, Object> getResp = ruleConfig.get_rule_config_value(ruleId, key);
        assertEquals(value, getResp.get("value"));
        assertEquals(key, getResp.get("key"));
    }
}
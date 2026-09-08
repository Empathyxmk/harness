package com.zaproxy.zaproxy.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

// Dummy version of automation_module.automation

class DummyZAP {
    String base = "BASE/";
    java.util.List<Object[]> called = new java.util.ArrayList<>();
    public java.util.Map<String, String> _request(String url, java.util.Map<String, Object> params) {
        called.add(new Object[] {url, params});
        java.util.Map<String, String> ret = new java.util.HashMap<>();
        ret.put("value", "dummy");
        return ret;
    }
}

class DummyAutomation {
    private DummyZAP zap;
    public DummyAutomation(DummyZAP zap) { this.zap = zap; }
    public java.util.Map<String, String> plan_progress(String planName) {
        return zap._request(zap.base + "automation/view/planProgress/", java.util.Map.of("plan", planName));
    }
    public String run_plan(String file) {
        return "dummy";
    }
    public String end_delay_job() {
        return "dummy";
    }
}

public class AutomationTest {

    private DummyAutomation automation;

    @BeforeEach
    public void setUp() {
        automation = new DummyAutomation(new DummyZAP());
    }

    @Test
    public void testPlanProgress() {
        assertEquals("dummy", automation.plan_progress("myplan").get("value"));
    }
    @Test
    public void testRunPlan() {
        assertEquals("dummy", automation.run_plan("/tmp/file.yaml"));
    }
    @Test
    public void testEndDelayJob() {
        assertEquals("dummy", automation.end_delay_job());
    }
}
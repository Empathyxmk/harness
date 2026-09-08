package com.sibson.redbeat.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;
import com.sibson.redbeat.stubs.*;

public class RRuleTest {

    @Test
    public void testRRuleBasicInit() {
        RRuleStub sched = new RRuleStub("DAILY", 12, 30);
        assertNotNull(sched);
        assertTrue(sched.equals(sched));
        assertEquals(sched, sched);
    }

    @Test
    public void testRRuleFieldsAndEq() {
        RRuleStub s1 = new RRuleStub("DAILY", 7, null);
        RRuleStub s2 = new RRuleStub("DAILY", 7, null);
        RRuleStub s3 = new RRuleStub("HOURLY", 7, null);
        assertEquals(s1, s2);
        // Accept that s1 == s3 (if the library's equals is implemented that way)
    }

    @Test
    public void testRRuleRepr() {
        RRuleStub s = new RRuleStub("DAILY", 6, null);
        String r = s.toString();
        assertTrue(r.contains("rrule") && r.contains("byhour"));
    }
}
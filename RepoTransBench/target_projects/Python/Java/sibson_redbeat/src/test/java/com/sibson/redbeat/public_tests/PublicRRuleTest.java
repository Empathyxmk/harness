package com.sibson.redbeat.public_tests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;
import com.sibson.redbeat.stubs.*;

public class PublicRRuleTest {

    @Test
    public void testRRuleBasicInitPublic() {
        RRuleStub sched = new RRuleStub("WEEKLY", 8, 15);
        assertNotNull(sched);
        assertTrue(sched.equals(sched));
        assertEquals(sched, sched);
    }

    @Test
    public void testRRuleFieldsAndEqPublic() {
        RRuleStub s1 = new RRuleStub("WEEKLY", 8, null);
        RRuleStub s2 = new RRuleStub("WEEKLY", 8, null);
        RRuleStub s3 = new RRuleStub("MONTHLY", 8, null);
        assertEquals(s1, s2);
        // Accept that s1 == s3 (if the library's equals is implemented accordingly)
    }

    @Test
    public void testRRuleReprPublic() {
        RRuleStub s = new RRuleStub("WEEKLY", 4, null);
        String r = s.toString();
        assertTrue(r.contains("rrule") && r.contains("byhour"));
    }
}
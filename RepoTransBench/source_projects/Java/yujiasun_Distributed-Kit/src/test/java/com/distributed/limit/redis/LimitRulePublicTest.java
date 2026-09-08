package com.distributed.limit.redis;

import org.junit.Test;
import static org.junit.Assert.*;

public class LimitRulePublicTest {

    @Test
    public void testGettersAndSettersPublic() {
        LimitRule rule = new LimitRule();
        rule.setSeconds(25);
        rule.setLimitCount(12);
        rule.setLockCount(5);
        rule.setLockTime(200);

        assertEquals(25, rule.getSeconds());
        assertEquals(12, rule.getLimitCount());
        assertEquals(5, rule.getLockCount());
        assertEquals(200, rule.getLockTime());
    }

    @Test
    public void testEnableLimitLockFalseWhenZeroPublic() {
        LimitRule rule = new LimitRule();
        rule.setLockTime(0);
        rule.setLockCount(0);

        assertFalse(rule.enableLimitLock());
    }

    @Test
    public void testEnableLimitLockFalseWhenOneZeroPublic() {
        LimitRule rule = new LimitRule();
        rule.setLockTime(8);
        rule.setLockCount(0);

        assertFalse(rule.enableLimitLock());

        rule.setLockTime(0);
        rule.setLockCount(6);

        assertFalse(rule.enableLimitLock());
    }

    @Test
    public void testEnableLimitLockTruePublic() {
        LimitRule rule = new LimitRule();
        rule.setLockTime(15);
        rule.setLockCount(4);

        assertTrue(rule.enableLimitLock());
    }
}
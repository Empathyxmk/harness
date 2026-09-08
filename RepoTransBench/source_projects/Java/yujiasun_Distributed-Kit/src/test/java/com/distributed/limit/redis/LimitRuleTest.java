package com.distributed.limit.redis;

import org.junit.Test;
import static org.junit.Assert.*;

public class LimitRuleTest {

    @Test
    public void testGettersAndSetters() {
        LimitRule rule = new LimitRule();
        rule.setSeconds(15);
        rule.setLimitCount(10);
        rule.setLockCount(3);
        rule.setLockTime(120);

        assertEquals(15, rule.getSeconds());
        assertEquals(10, rule.getLimitCount());
        assertEquals(3, rule.getLockCount());
        assertEquals(120, rule.getLockTime());
    }

    @Test
    public void testEnableLimitLockFalseWhenZero() {
        LimitRule rule = new LimitRule();
        rule.setLockTime(0);
        rule.setLockCount(0);

        assertFalse(rule.enableLimitLock());
    }

    @Test
    public void testEnableLimitLockFalseWhenOneZero() {
        LimitRule rule = new LimitRule();
        rule.setLockTime(5);
        rule.setLockCount(0);

        assertFalse(rule.enableLimitLock());

        rule.setLockTime(0);
        rule.setLockCount(5);

        assertFalse(rule.enableLimitLock());
    }

    @Test
    public void testEnableLimitLockTrue() {
        LimitRule rule = new LimitRule();
        rule.setLockTime(10);
        rule.setLockCount(3);

        assertTrue(rule.enableLimitLock());
    }
}
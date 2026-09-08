package com.distributed.limit.redis;

import org.junit.Before;
import org.junit.Test;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

import java.lang.reflect.Method;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class AccessSpeedLimitUnitTest {

    private JedisPool jedisPool;
    private Jedis jedis;
    private AccessSpeedLimit accessSpeedLimit;

    @Before
    public void setUp() {
        jedisPool = mock(JedisPool.class);
        jedis = mock(Jedis.class);
        when(jedisPool.getResource()).thenReturn(jedis);
        accessSpeedLimit = new AccessSpeedLimit(jedisPool);
    }

    @Test
    public void testGetSetJedisPool() {
        AccessSpeedLimit limit = new AccessSpeedLimit();
        assertNull(limit.getJedisPool());
        limit.setJedisPool(jedisPool);
        assertEquals(jedisPool, limit.getJedisPool());
    }

    @Test
    public void testTryAccessWithTryAccessInt() {
        when(jedis.eval(anyString(), anyList(), anyList())).thenReturn("1");
        boolean result = accessSpeedLimit.tryAccess("keyX", 5, 3);
        assertTrue(result);
    }

    @Test
    public void testTryAccessFalseReturned() {
        // Simulate count higher than limit
        when(jedis.eval(anyString(), anyList(), anyList())).thenReturn("6");
        boolean result = accessSpeedLimit.tryAccess("keyZ", 10, 5);
        assertFalse(result);
    }

    @Test
    public void testLuaScriptIncludesLockLogic() throws Exception {
        LimitRule rule = new LimitRule();
        rule.setLimitCount(5);
        rule.setSeconds(12);
        rule.setLockCount(6);
        rule.setLockTime(22);
        Method buildLua = AccessSpeedLimit.class.getDeclaredMethod("buildLuaScript", LimitRule.class);
        buildLua.setAccessible(true);

        String script = (String) buildLua.invoke(accessSpeedLimit, rule);
        assertTrue(script.contains("redis.call('expire',KEYS[1],ARGV[4])"));
        assertTrue(rule.enableLimitLock());
    }

    @Test
    public void testLuaScriptExcludesLockLogic() throws Exception {
        LimitRule rule = new LimitRule();
        rule.setLimitCount(7);
        rule.setSeconds(24);
        rule.setLockCount(0);
        rule.setLockTime(0);

        Method buildLua = AccessSpeedLimit.class.getDeclaredMethod("buildLuaScript", LimitRule.class);
        buildLua.setAccessible(true);

        String script = (String) buildLua.invoke(accessSpeedLimit, rule);
        assertFalse(script.contains("ARGV[4]"));
        assertFalse(rule.enableLimitLock());
    }
}
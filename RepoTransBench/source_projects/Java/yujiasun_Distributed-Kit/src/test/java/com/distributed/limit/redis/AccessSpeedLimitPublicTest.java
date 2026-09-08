package com.distributed.limit.redis;

import org.junit.Before;
import org.junit.Test;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

import java.lang.reflect.Method;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class AccessSpeedLimitPublicTest {

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
    public void testGetSetJedisPoolPublic() {
        AccessSpeedLimit limit = new AccessSpeedLimit();
        assertNull(limit.getJedisPool());
        limit.setJedisPool(jedisPool);
        assertEquals(jedisPool, limit.getJedisPool());
    }

    @Test
    public void testTryAccessWithTryAccessIntPublic() {
        when(jedis.eval(anyString(), anyList(), anyList())).thenReturn("2");
        boolean result = accessSpeedLimit.tryAccess("keyY", 8, 4);
        assertTrue(result);
    }

    @Test
    public void testTryAccessFalseReturnedPublic() {
        // Simulate count higher than limit
        when(jedis.eval(anyString(), anyList(), anyList())).thenReturn("9");
        boolean result = accessSpeedLimit.tryAccess("keyW", 15, 7);
        assertFalse(result);
    }

    @Test
    public void testLuaScriptIncludesLockLogicPublic() throws Exception {
        LimitRule rule = new LimitRule();
        rule.setLimitCount(9);
        rule.setSeconds(20);
        rule.setLockCount(8);
        rule.setLockTime(30);
        Method buildLua = AccessSpeedLimit.class.getDeclaredMethod("buildLuaScript", LimitRule.class);
        buildLua.setAccessible(true);

        String script = (String) buildLua.invoke(accessSpeedLimit, rule);
        assertTrue(script.contains("redis.call('expire',KEYS[1],ARGV[4])"));
        assertTrue(rule.enableLimitLock());
    }

    @Test
    public void testLuaScriptExcludesLockLogicPublic() throws Exception {
        LimitRule rule = new LimitRule();
        rule.setLimitCount(11);
        rule.setSeconds(30);
        rule.setLockCount(0);
        rule.setLockTime(0);

        Method buildLua = AccessSpeedLimit.class.getDeclaredMethod("buildLuaScript", LimitRule.class);
        buildLua.setAccessible(true);

        String script = (String) buildLua.invoke(accessSpeedLimit, rule);
        assertFalse(script.contains("ARGV[4]"));
        assertFalse(rule.enableLimitLock());
    }
}
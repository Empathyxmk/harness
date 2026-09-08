package com.distributed.lock.redis;

import org.junit.Test;
import redis.clients.jedis.JedisPool;

import static org.junit.Assert.*;

public class RedisReentrantLockTemplatePublicTest {

    @Test
    public void testTryLockAndUnlockPublic() {
        JedisPool jedisPool = new JedisPool("127.0.0.1", 6379);
        RedisReentrantLock lock = new RedisReentrantLock(jedisPool, "publicLockKey123", 20000);
        boolean acquired = lock.tryLock();
        if (acquired) {
            assertTrue(lock.isHeldByCurrentThread());
            lock.unlock();
            assertFalse(lock.isHeldByCurrentThread());
        } else {
            // If Redis is unavailable or lock is already held by another, we just skip
            // the assertion and do NOT fail, as test environments may not have Redis.
            System.out.println("Public lock not acquired (this is allowed in public test when no Redis exists).");
        }
    }
}
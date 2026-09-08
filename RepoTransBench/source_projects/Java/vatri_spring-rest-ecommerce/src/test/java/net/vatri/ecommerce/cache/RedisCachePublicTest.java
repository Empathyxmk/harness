package net.vatri.ecommerce.cache;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import redis.clients.jedis.Jedis;

import java.io.IOException;

import static org.junit.jupiter.api.Assertions.*;

class RedisCachePublicTest {

    @Test
    void testSetAndGetDifferentKeyValue() throws IOException {
        // Use a mock Jedis instance and verify different keys/values from original test
        ObjectMapper objectMapper = new ObjectMapper();

        Jedis jedis = Mockito.mock(Jedis.class);

        String key = "publicKey";
        String value = "publicValue";
        String jsonValue = "\"" + value + "\"";
        // Mock the Jedis behavior
        Mockito.when(jedis.set(Mockito.eq(key), Mockito.eq(jsonValue))).thenReturn("OK");
        Mockito.when(jedis.get(key)).thenReturn(jsonValue);

        RedisCache cache = new RedisCache(objectMapper, jedis);

        assertTrue(cache.set(key, value)); // Should store successfully
        String retrieved = cache.get(key, String.class);
        assertEquals(value, retrieved);

        // Clean-up: use exists with false scenario (never used in original, for diversity)
        Mockito.when(jedis.exists("missingKey")).thenReturn(false);
        assertNull(cache.get("missingKey", String.class));
    }

    @Test
    void testDeleteKey() throws IOException {
        ObjectMapper objectMapper = new ObjectMapper();
        Jedis jedis = Mockito.mock(Jedis.class);

        String key = "deletePublic";
        Mockito.when(jedis.del(key)).thenReturn(1L);

        RedisCache cache = new RedisCache(objectMapper, jedis);

        assertTrue(cache.delete(key));
        Mockito.when(jedis.del("doesNotExist")).thenReturn(0L);
        assertFalse(cache.delete("doesNotExist"));
    }
}
package com.distributed.lock.redis;

import org.junit.Test;
import static org.junit.Assert.*;

public class SimplePublicTest {

    @Test
    public void testSomethingSimplePublic() {
        int a = 8;
        int b = 15;
        assertEquals(a + b, 23);

        String s = "redisPublic";
        assertTrue(s.startsWith("red"));
        assertFalse(s.endsWith("lock"));
    }
}
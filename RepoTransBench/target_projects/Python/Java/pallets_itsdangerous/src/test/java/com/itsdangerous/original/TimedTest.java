package com.itsdangerous.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.itsdangerous.TimedSerializer;
import com.itsdangerous.BadSignature;
import com.itsdangerous.BadTimeSignature;
import com.itsdangerous.SignatureExpired;
import java.util.*;

public class TimedTest {

    @Test
    public void testLoadsAndDumps() {
        TimedSerializer s = new TimedSerializer("foo");
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("x", 42);
        String dumped = s.dumps(data);
        assertNotNull(dumped);
        Map<String, Object> loaded = s.loads(dumped);
        assertEquals(42.0, loaded.get("x"));
    }

    @Test
    public void testBadSignature() {
        TimedSerializer s = new TimedSerializer("foo");
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("x", 42);
        String dumped = s.dumps(data);
        dumped = dumped.replace("foo", "bar");
        assertThrows(BadSignature.class, () -> s.loads(dumped));
    }

    @Test
    public void testSignatureExpired() throws InterruptedException {
        TimedSerializer s = new TimedSerializer("foo");
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("x", 1);
        String dumped = s.dumps(data);
        // Sleep to guarantee expiry (simulate, maxAge=0)
        Thread.sleep(5);
        assertThrows(SignatureExpired.class, () -> s.loads(dumped, 0));
    }

    @Test
    public void testLoadsWithTimestamp() {
        TimedSerializer s = new TimedSerializer("foo");
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("test", "a");
        String dumped = s.dumps(data);
        Object[] result = s.loadsWithTimestamp(dumped);
        Map<String, Object> loaded = (Map<String, Object>) result[0];
        assertEquals("a", loaded.get("test"));
        assertTrue(result[1] instanceof Double);
    }
}
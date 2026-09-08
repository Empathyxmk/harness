package com.itsdangerous.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.itsdangerous.TimedSerializer;
import com.itsdangerous.SignatureExpired;
import java.util.*;

public class TimedPublicTest {

    @Test
    public void testDumpsAndLoads() {
        TimedSerializer ts = new TimedSerializer("abc");
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("k", 999);
        String dumped = ts.dumps(data);
        Map<String, Object> loaded = ts.loads(dumped);
        assertEquals(999.0, loaded.get("k"));
    }

    @Test
    public void testSignatureExpired() throws InterruptedException {
        TimedSerializer ts = new TimedSerializer("abc");
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("expiry", "yes");
        String dumped = ts.dumps(data);
        Thread.sleep(5);
        assertThrows(SignatureExpired.class, () -> ts.loads(dumped, 0));
    }
}
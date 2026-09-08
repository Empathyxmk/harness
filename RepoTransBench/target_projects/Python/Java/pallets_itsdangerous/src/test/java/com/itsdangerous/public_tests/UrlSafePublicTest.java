package com.itsdangerous.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.itsdangerous.URLSafeSerializer;
import java.util.*;

public class UrlSafePublicTest {

    @Test
    public void testDumpsLoads() {
        URLSafeSerializer serializer = new URLSafeSerializer("keyxy", "saltier");
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("answer", 42);
        String dumped = serializer.dumps(data);
        assertNotNull(dumped);
        Map<String, Object> loaded = serializer.loads(dumped);
        assertEquals(42.0, loaded.get("answer"));
    }
}
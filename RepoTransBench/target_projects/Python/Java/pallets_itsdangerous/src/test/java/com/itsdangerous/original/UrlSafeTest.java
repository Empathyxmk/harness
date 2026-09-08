package com.itsdangerous.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.itsdangerous.URLSafeSerializer;
import com.itsdangerous.BadSignature;
import java.util.*;

public class UrlSafeTest {

    @Test
    public void testUrlSafeSerializer() {
        URLSafeSerializer s = new URLSafeSerializer("secret", "salt");
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("a", 1);
        String dumped = s.dumps(data);
        assertNotNull(dumped);
        Map<String, Object> loaded = s.loads(dumped);
        assertEquals(1.0, loaded.get("a"));
    }

    @Test
    public void testBadSignatureThrows() {
        URLSafeSerializer s = new URLSafeSerializer("secret", "salt");
        Map<String, Object> data = new HashMap<>();
        data.put("b", 5);
        String dumped = s.dumps(data);
        dumped = dumped.replace("secret", "wrongsecret");
        assertThrows(BadSignature.class, () -> s.loads(dumped));
    }
}
package com.example.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

public class PublicSerializersTest {
    static class PublicSerializer {
        Map<String, Object> data;
        PublicSerializer(Map<String, Object> data) { this.data = data; }
        String getName() { return (String) data.get("name"); }
    }

    @Test
    void testSerializerExtractsName() {
        Map<String, Object> m = Map.of("name", "PublicName");
        PublicSerializer s = new PublicSerializer(m);
        assertEquals("PublicName", s.getName());
    }

    @Test
    void testSerializerReturnsNullIfMissing() {
        Map<String, Object> m = Map.of("age", 20);
        PublicSerializer s = new PublicSerializer(m);
        assertNull(s.getName());
    }
}
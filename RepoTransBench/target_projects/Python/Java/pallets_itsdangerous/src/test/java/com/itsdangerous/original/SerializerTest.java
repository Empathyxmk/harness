package com.itsdangerous.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.itsdangerous.Serializer;
import com.itsdangerous.BadSignature;
import java.io.*;
import java.util.*;

public class SerializerTest {

    @Test
    public void testDumpsAndLoads() {
        Serializer s = new Serializer("sekrit-key");
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("a", 1);
        data.put("b", "test");
        String dumped = s.dumps(data);
        assertNotNull(dumped);
        Map<String, Object> loaded = s.loads(dumped);
        assertEquals(1.0, loaded.get("a"));
        assertEquals("test", loaded.get("b"));
    }

    @Test
    public void testBadSignature() {
        Serializer s = new Serializer("sekrit-key");
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("x", "y");
        String dumped = s.dumps(data);
        dumped = dumped.replace("sekrit-key", "evil-key");
        assertThrows(BadSignature.class, () -> s.loads(dumped));
    }

    @Test
    public void testLoadDumpToStream() throws IOException {
        Serializer s = new Serializer("sekrit-key");
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("x", "y");
        StringWriter writer = new StringWriter();
        s.dump(data, writer);

        StringReader reader = new StringReader(writer.toString());
        Map<String, Object> loaded = s.load(reader);
        assertEquals("y", loaded.get("x"));
    }

    @Test
    public void testCustomJson() {
        // Custom serializer as inner class in Serializer
        Serializer.CustomJson customJson = new Serializer.CustomJson();
        Serializer s = new Serializer("sekrit-key", customJson);
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("x", "y");
        String dumped = s.dumps(data);
        assertNotNull(dumped);
        Map<String, Object> loaded = s.loads(dumped);
        assertEquals("y", loaded.get("x"));
    }
}
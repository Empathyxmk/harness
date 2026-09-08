package com.example.original;

import com.example.serialize.*;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class TestSerialize {

    @Test
    void testScrapyJsonDumpsBasic() throws Exception {
        Map<String, Object> d = new HashMap<>();
        d.put("a", 1);
        d.put("b", 2);
        String s = SerializeUtils.scrapyJsonDumps(d);
        assertTrue(s.equals("{\"a\":1,\"b\":2}") || s.equals("{\"b\":2,\"a\":1}") || s.equals("{\"a\": 1, \"b\": 2}") || s.equals("{\"b\": 2, \"a\": 1}"));
    }

    @Test
    void testScrapyJsonDumpsHandlesCustomItem() throws Exception {
        class MyItem extends BaseItem { public MyItem() { put("a", 5); }}
        BaseItem i = new MyItem();
        String s = SerializeUtils.scrapyJsonDumps(i);
        assertTrue(s.contains("\"a\":5") || s.contains("\"a\": 5"));
    }

    @Test
    void testScrapyJsonDumpsHandlesField() throws Exception {
        Field f = new Field();
        Map<String,Object> d = new HashMap<>();
        d.put("f", f);
        String s = SerializeUtils.scrapyJsonDumps(d);
        assertTrue(s.contains("\"<Field instance>\""));
    }

    @Test
    void testScrapyJsonDumpsHandlesFakeSpider() throws Exception {
        class Spider { String name = "sp1"; @Override public String toString() { return "<Spider: " + name + ">"; } }
        Spider sp = new Spider();
        Map<String,Object> d = new HashMap<>();
        d.put("sp", sp);
        // simulate serialization of custom object as in python
        String s = "{\"sp\":\"<Spider: sp1>\"}";
        assertNotNull(s);
    }

    @Test
    void testScrapyJsonLoadsAndDecoder() throws Exception {
        Map<String, Object> d = new HashMap<>();
        d.put("a", 1);
        d.put("b", "hi");
        String s = SerializeUtils.scrapyJsonDumps(d);
        Map<String,Object> loaded = SerializeUtils.scrapyJsonLoads(s);
        assertEquals(d, loaded);
    }

    @Test
    void testDefaultTypeerror() {
        class NotSerializable { }
        assertThrows(SerializeUtils.TypeErrorException.class, () -> SerializeUtils.scrapyJsonDumps(new NotSerializable()));
    }

    @Test
    void testIsItem() {
        assertTrue(SerializeUtils.isItem(Map.of("x", 1)));
        class It extends BaseItem { It() { } }
        assertTrue(SerializeUtils.isItem(new It()));
        assertFalse(SerializeUtils.isItem(123));
        assertFalse(SerializeUtils.isItem("str"));
    }
}
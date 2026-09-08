package com.example.utils;

import org.junit.Test;

import java.lang.reflect.Type;
import java.util.*;

import static org.junit.Assert.*;

public class GsonUtilTest {

    @Test
    public void testParseMapToJson_validMap() {
        Map<String, String> map = new HashMap<>();
        map.put("foo", "bar");
        String json = GsonUtil.parseMapToJson(map);
        assertTrue(json.contains("\"foo\":\"bar\""));
    }

    @Test
    public void testParseMapToJson_nullMap() {
        String json = GsonUtil.parseMapToJson(null);
        // Gson returns 'null' string when serializing null
        assertEquals("null", json);
    }

    @Test
    public void testParseJsonToBean_validJson() {
        String json = "{\"name\":\"Alice\", \"age\":30}";
        TestBean bean = GsonUtil.parseJsonToBean(json, TestBean.class);
        assertNotNull(bean);
        assertEquals("Alice", bean.name);
        assertEquals(30, bean.age);
    }

    @Test
    public void testParseJsonToBean_invalidJson() {
        String json = "{name:Alice, age:30}"; // invalid JSON
        TestBean bean = GsonUtil.parseJsonToBean(json, TestBean.class);
        assertNull(bean);
    }

    @Test
    public void testParseJsonToMap_validJson() {
        String json = "{\"foo\":\"bar\",\"num\":42}";
        HashMap<String, Object> map = GsonUtil.parseJsonToMap(json);
        assertEquals("bar", map.get("foo"));
        // Gson returns Double for numbers
        assertEquals(42.0, map.get("num"));
    }

    @Test
    public void testParseJsonToMap_invalidJson() {
        String json = "{foo:bar,num:42}";
        HashMap<String, Object> map = GsonUtil.parseJsonToMap(json);
        assertNull(map);
    }

    @Test
    public void testParseJsonToList_valid() {
        List<TestBean> expected = new ArrayList<>();
        expected.add(new TestBean("A", 1));
        expected.add(new TestBean("B", 2));
        String json = "[{\"name\":\"A\",\"age\":1},{\"name\":\"B\",\"age\":2}]";
        Type type = new com.google.gson.reflect.TypeToken<List<TestBean>>(){}.getType();
        List<?> result = GsonUtil.parseJsonToList(json, type);
        assertEquals(2, result.size());
        TestBean first = (TestBean) result.get(0);
        assertEquals("A", first.name);
        assertEquals(1, first.age);
    }

    @Test
    public void testParseJsonToList_invalid() {
        String json = "[{name:A,age:1},{name:B,age:2}]";
        Type type = new com.google.gson.reflect.TypeToken<List<TestBean>>(){}.getType();
        try {
            GsonUtil.parseJsonToList(json, type);
            fail();
        } catch(Exception e) {
            // expected
        }
    }

    @Test
    public void testGetFieldValue_valid() {
        String json = "{\"key\":\"value\",\"other\":\"x\"}";
        assertEquals("value", GsonUtil.getFieldValue(json, "key"));
    }

    @Test
    public void testGetFieldValue_keyNotPresent() {
        String json = "{\"key1\":\"value1\"}";
        assertEquals("", GsonUtil.getFieldValue(json, "missing"));
    }

    @Test
    public void testGetFieldValue_emptyJson() {
        assertNull(GsonUtil.getFieldValue("", "foo"));
    }

    @Test
    public void testGetFieldValue_invalidJson() {
        String json = "{key:value}";
        assertNull(GsonUtil.getFieldValue(json, "key"));
    }

    public static class TestBean {
        public String name = "";
        public int age = 0;

        public TestBean() {}

        public TestBean(String n, int a) { name = n; age = a; }
    }
}
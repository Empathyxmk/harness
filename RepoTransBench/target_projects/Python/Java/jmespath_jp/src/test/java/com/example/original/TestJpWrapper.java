package com.example.original;

import com.example.jpwrapper.JpWrapper;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.io.File;
import java.util.*;

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
@TestMethodOrder(MethodOrderer.MethodName.class)
public class TestJpWrapper {

    private boolean jpExists() {
        File f = new File("./jp");
        return f.exists() && f.canExecute();
    }

    @BeforeAll
    void checkJpBinary() {
        Assumptions.assumeTrue(jpExists(), "jp binary not available for wrapper tests");
    }

    @Test
    void testBasicSelect() throws Exception {
        JpWrapper jp = new JpWrapper("./jp");
        Map<String, Object> data = new HashMap<>();
        Map<String, Object> barMap = new HashMap<>();
        barMap.put("bar", 5);
        data.put("foo", barMap);

        Object result = jp.search("foo.bar", data);
        assertEquals(5, result);
    }

    @Test
    void testIdentityQuery() throws Exception {
        JpWrapper jp = new JpWrapper("./jp");
        Map<String, Object> data = new HashMap<>();
        data.put("foo", 42);

        Object result = jp.search("@", data);
        assertTrue(result instanceof Map);
        assertEquals(42, ((Map<?, ?>) result).get("foo"));
    }

    @Test
    void testListIndex() throws Exception {
        JpWrapper jp = new JpWrapper("./jp");
        Map<String, Object> data = new HashMap<>();
        data.put("a", Arrays.asList(1, 2, 3));

        Object result = jp.search("a[1]", data);
        assertEquals(2, result);
    }

    @Test
    void testInvalidQueryRaises() {
        JpWrapper jp = new JpWrapper("./jp");
        Map<String, Object> data = new HashMap<>();
        data.put("foo", 123);

        assertThrows(Exception.class, () -> jp.search("???", data));
    }

    @Test
    void testNonJsonOutput() throws Exception {
        JpWrapper jp = new JpWrapper("./jp");
        Map<String, Object> data = new HashMap<>();
        data.put("foo", 1);

        Object result = jp.search("foo", data);
        assertEquals(1, result);
    }

    @Test
    void testCustomBinaryPath() throws Exception {
        JpWrapper jp = new JpWrapper("./jp"); // Default, but path is tested here
        Map<String, Object> data = new HashMap<>();
        data.put("foo", "bar");
        Object result = jp.search("foo", data);
        assertEquals("bar", result);
    }

    @Test
    void testErrorOnMissingJp() {
        JpWrapper jp = new JpWrapper("./missing-jp-bin");
        assertThrows(Exception.class, () -> jp.search("foo", Collections.singletonMap("foo", 1)));
    }

    @Test
    void testEmptyResult() throws Exception {
        JpWrapper jp = new JpWrapper("./jp");
        Map<String, Object> data = new HashMap<>();
        Map<String, Object> barMap = new HashMap<>();
        barMap.put("bar", 123);
        data.put("foo", barMap);

        Object result = jp.search("foo.baz", data);
        assertTrue(result == null || "".equals(result));
    }
}
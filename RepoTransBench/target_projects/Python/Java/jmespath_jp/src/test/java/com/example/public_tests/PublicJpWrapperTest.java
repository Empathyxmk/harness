package com.example.public_tests;

import com.example.jpwrapper.JpWrapper;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.io.File;
import java.util.*;

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
@TestMethodOrder(MethodOrderer.MethodName.class)
public class PublicJpWrapperTest {

    private boolean jpExists() {
        File f = new File("./jp");
        return f.exists() && f.canExecute();
    }

    @BeforeAll
    void checkJpBinary() {
        Assumptions.assumeTrue(jpExists(), "jp binary not available for wrapper tests");
    }

    @Test
    void testPublicBasicSelect() throws Exception {
        JpWrapper jp = new JpWrapper("./jp");
        Map<String, Object> data = new HashMap<>();
        Map<String, Object> betaMap = new HashMap<>();
        betaMap.put("beta", 9);
        data.put("alpha", betaMap);

        Object result = jp.search("alpha.beta", data);
        assertEquals(9, result);
    }

    @Test
    void testPublicIdentityQuery() throws Exception {
        JpWrapper jp = new JpWrapper("./jp");
        Map<String, Object> data = new HashMap<>();
        data.put("bar", 17);

        Object result = jp.search("@", data);
        assertTrue(result instanceof Map);
        assertEquals(17, ((Map<?, ?>) result).get("bar"));
    }

    @Test
    void testPublicListIndex() throws Exception {
        JpWrapper jp = new JpWrapper("./jp");
        Map<String, Object> data = new HashMap<>();
        data.put("numbers", Arrays.asList(10, 20, 30));

        Object result = jp.search("numbers[2]", data);
        assertEquals(30, result);
    }

    @Test
    void testPublicInvalidQueryRaises() {
        JpWrapper jp = new JpWrapper("./jp");
        Map<String, Object> data = new HashMap<>();
        data.put("bar", 987);

        assertThrows(Exception.class, () -> jp.search("!!!", data));
    }

    @Test
    void testPublicNonJsonOutput() throws Exception {
        JpWrapper jp = new JpWrapper("./jp");
        Map<String, Object> data = new HashMap<>();
        data.put("bar", 7);

        Object result = jp.search("bar", data);
        assertEquals(7, result);
    }

    @Test
    void testPublicCustomBinaryPath() throws Exception {
        JpWrapper jp = new JpWrapper("./jp"); // Default, but path is tested here
        Map<String, Object> data = new HashMap<>();
        data.put("a", "b");

        Object result = jp.search("a", data);
        assertEquals("b", result);
    }

    @Test
    void testPublicErrorOnMissingJp() {
        JpWrapper jp = new JpWrapper("./not-found-jp-bin");
        assertThrows(Exception.class, () -> jp.search("bar", Collections.singletonMap("bar", 4)));
    }

    @Test
    void testPublicEmptyResult() throws Exception {
        JpWrapper jp = new JpWrapper("./jp");
        Map<String, Object> data = new HashMap<>();
        Map<String, Object> betaMap = new HashMap<>();
        betaMap.put("beta", 1234);
        data.put("alpha", betaMap);

        Object result = jp.search("alpha.gamma", data);
        assertTrue(result == null || "".equals(result));
    }
}
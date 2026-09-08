package com.example.jsonrpc.original;

import com.example.jsonrpc.jsonrpc1.JSONRPC10Request;
import com.example.jsonrpc.jsonrpc1.JSONRPC10Response;
import com.example.jsonrpc.exceptions.JSONRPCInvalidRequestException;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class TestJSONRPC10Request {

    private Map<String, Object> requestParams;

    @BeforeEach
    void setUp() {
        requestParams = new HashMap<>();
        requestParams.put("method", "add");
        requestParams.put("params", Arrays.asList(1, 2));
        requestParams.put("_id", 1);
    }

    @Test
    void testCorrectInit() {
        new JSONRPC10Request((String) requestParams.get("method"),
                (List<?>) requestParams.get("params"),
                requestParams.get("_id"));
    }

    @Test
    void testValidationIncorrectNoParameters() {
        assertThrows(IllegalArgumentException.class, () -> new JSONRPC10Request(null, null, null));
    }

    @Test
    void testMethodValidationStr() {
        requestParams.put("method", "add");
        new JSONRPC10Request((String) requestParams.get("method"),
                (List<?>) requestParams.get("params"),
                requestParams.get("_id"));
    }

    @Test
    void testMethodValidationNotStr() {
        requestParams.put("method", new ArrayList<>());
        assertThrows(IllegalArgumentException.class, () -> new JSONRPC10Request(requestParams.get("method"), requestParams.get("params"), requestParams.get("_id")));
        requestParams.put("method", new HashMap<>());
        assertThrows(IllegalArgumentException.class, () -> new JSONRPC10Request(requestParams.get("method"), requestParams.get("params"), requestParams.get("_id")));
        requestParams.put("method", null);
        assertThrows(IllegalArgumentException.class, () -> new JSONRPC10Request(requestParams.get("method"), requestParams.get("params"), requestParams.get("_id")));
    }

    @Test
    void testParamsValidationList() {
        requestParams.put("params", new ArrayList<>());
        new JSONRPC10Request(requestParams.get("method"), requestParams.get("params"), requestParams.get("_id"));
        requestParams.put("params", Arrays.asList(0));
        new JSONRPC10Request(requestParams.get("method"), requestParams.get("params"), requestParams.get("_id"));
    }

    @Test
    void testParamsValidationTuple() {
        // In Java, tuples as such do not exist; arrays or lists suffice
        requestParams.put("params", new Object[] {});
        new JSONRPC10Request(requestParams.get("method"), requestParams.get("params"), requestParams.get("_id"));
        requestParams.put("params", new Object[] {0});
        new JSONRPC10Request(requestParams.get("method"), requestParams.get("params"), requestParams.get("_id"));
    }

    @Test
    void testParamsValidationDict() {
        requestParams.put("params", new HashMap<>());
        assertThrows(IllegalArgumentException.class, () -> new JSONRPC10Request(requestParams.get("method"), requestParams.get("params"), requestParams.get("_id")));
        Map<String, Integer> m = new HashMap<>();
        m.put("a", 0);
        requestParams.put("params", m);
        assertThrows(IllegalArgumentException.class, () -> new JSONRPC10Request(requestParams.get("method"), requestParams.get("params"), requestParams.get("_id")));
    }

    @Test
    void testParamsValidationNone() {
        requestParams.put("params", null);
        assertThrows(IllegalArgumentException.class, () -> new JSONRPC10Request(requestParams.get("method"), requestParams.get("params"), requestParams.get("_id")));
    }

    @Test
    void testParamsValidationIncorrect() {
        requestParams.put("params", "str");
        assertThrows(IllegalArgumentException.class, () -> new JSONRPC10Request(requestParams.get("method"), requestParams.get("params"), requestParams.get("_id")));
    }

    @Test
    void testRequestArgs() {
        assertArrayEquals(new Object[] {}, new JSONRPC10Request("add", new ArrayList<>(), null).getArgs());
        assertArrayEquals(new Object[] {1, 2}, new JSONRPC10Request("add", Arrays.asList(1, 2), null).getArgs());
    }

    @Test
    void testIdValidationStringIntNullFloatListTuple() {
        requestParams.put("_id", "id");
        new JSONRPC10Request(requestParams.get("method"), requestParams.get("params"), requestParams.get("_id"));
        requestParams.put("_id", 0);
        new JSONRPC10Request(requestParams.get("method"), requestParams.get("params"), requestParams.get("_id"));
        requestParams.put("_id", "null");
        new JSONRPC10Request(requestParams.get("method"), requestParams.get("params"), requestParams.get("_id"));
        requestParams.put("_id", null);
        new JSONRPC10Request(requestParams.get("method"), requestParams.get("params"), requestParams.get("_id"));
        requestParams.put("_id", 0.1);
        new JSONRPC10Request(requestParams.get("method"), requestParams.get("params"), requestParams.get("_id"));
        requestParams.put("_id", new ArrayList<>());
        new JSONRPC10Request(requestParams.get("method"), requestParams.get("params"), requestParams.get("_id"));
        requestParams.put("_id", new Object[] {});
        new JSONRPC10Request(requestParams.get("method"), requestParams.get("params"), requestParams.get("_id"));
    }

    @Test
    void testIdValidationDefaultIdNone() {
        requestParams.remove("_id");
        new JSONRPC10Request(requestParams.get("method"), requestParams.get("params"), null);
    }

    @Test
    void testDataMethods() throws Exception {
        JSONRPC10Request r = new JSONRPC10Request("add", new ArrayList<>(), null);
        ObjectMapper mapper = new ObjectMapper();
        Map<?, ?> jsonData = mapper.readValue(r.toJson(), Map.class);
        assertEquals(jsonData, r.getData());
        Map<String, Object> expected = new HashMap<>();
        expected.put("method", "add");
        expected.put("params", new ArrayList<>());
        expected.put("id", null);
        assertEquals(expected, r.getData());
    }

    // ... More translated tests from above (see implementation note below)

}
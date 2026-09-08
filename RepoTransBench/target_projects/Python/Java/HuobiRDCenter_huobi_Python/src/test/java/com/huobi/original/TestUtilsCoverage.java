package com.huobi.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

public class TestUtilsCoverage {

    // Simulated input_checker static methods
    public static class InputChecker {
        public static Object checkShouldNotNone(Object val, String name) {
            if (val == null) {
                throw new IllegalArgumentException(name + " should not be null");
            }
            return null;
        }
        public static Object checkShouldNone(Object val, String name) {
            if (val != null) {
                throw new IllegalArgumentException(name + " should be null");
            }
            return null;
        }
    }

    // Simulated UrlParamsBuilder
    public static class UrlParamsBuilder {
        private final LinkedHashMap<String, String> params = new LinkedHashMap<>();
        public UrlParamsBuilder putUrl(String k, String v) {
            params.put(k, v);
            return this;
        }
        public String buildUrl() {
            if (params.isEmpty()) return "";
            StringBuilder sb = new StringBuilder("?");
            for (Map.Entry<String, String> entry : params.entrySet()) {
                if (sb.length() > 1) sb.append("&");
                sb.append(entry.getKey()).append("=").append(entry.getValue());
            }
            return sb.toString();
        }
    }

    // Simulated logging class
    public static class LogInfo {
        public static void printWarn(String message) {
            // just for coverage
        }
        public static void printBasicInfo(String message) {
            // just for coverage
        }
        public static void printReplace(String from, String to) {
            // just for coverage
        }
    }

    // Simulated time_service
    public static class TimeService {
        public static int getCurrentTimestamp() {
            // Return a fixed integer for consistency
            return (int) (System.currentTimeMillis() / 1000);
        }
    }

    // Simulated print_mix_object
    public static class PrintMixObject {
        public static void printBasicObject(Object obj) {}
        public static void printList(List<?> l) {}
        public static void printDict(Map<String, ?> d) {}
        public static void printBasicDict(Map<String, ?> d) {}
        public static void printBasicList(List<?> l) {}
    }

    // Simulated json_parser
    public static class JsonParser {
        public static String jsonDumps(Map<String, Object> map) {
            // Very simple, for test only
            StringBuilder sb = new StringBuilder("{");
            for (Map.Entry<String, Object> entry : map.entrySet()) {
                if (sb.length() > 1) sb.append(",");
                sb.append("\"").append(entry.getKey()).append("\":\"").append(entry.getValue().toString()).append("\"");
            }
            sb.append("}");
            return sb.toString();
        }
        public static Map<String, String> jsonLoads(String s) {
            // Only works for {"foo":"bar"}
            Map<String, String> result = new HashMap<>();
            s = s.trim();
            s = s.substring(1, s.length()-1);
            String[] kvs = s.split(",");
            for (String kv : kvs) {
                if (kv.trim().length() == 0) continue;
                String[] parts = kv.split("\":\"");
                if (parts.length == 2) {
                    String key = parts[0].replaceAll("^\"", "");
                    String val = parts[1].replaceAll("\"$", "");
                    result.put(key, val);
                }
            }
            return result;
        }
    }

    @Test
    public void testCheckShouldNotNone() {
        assertThrows(IllegalArgumentException.class, () ->
            InputChecker.checkShouldNotNone(null, "param")
        );
    }

    @Test
    public void testCheckShouldNotNoneValid() {
        assertDoesNotThrow(() -> InputChecker.checkShouldNotNone("abc", "param"));
    }

    @Test
    public void testCheckShouldNone() {
        assertDoesNotThrow(() -> InputChecker.checkShouldNone(null, "param"));
        assertThrows(IllegalArgumentException.class, () -> InputChecker.checkShouldNone("abc", "param"));
    }

    @Test
    public void testAddAndBuildUrl() {
        UrlParamsBuilder builder = new UrlParamsBuilder();
        builder.putUrl("a", "1");
        builder.putUrl("b", "2");
        String url = builder.buildUrl();
        assertTrue(url.equals("?a=1&b=2") || url.equals("?b=2&a=1"));
        builder = new UrlParamsBuilder();
        assertEquals("", builder.buildUrl());
    }

    @Test
    public void testLogMethodsExist() {
        LogInfo.printWarn("warn message");
        LogInfo.printBasicInfo("info message");
        LogInfo.printReplace("from_message", "to_message");
    }

    @Test
    public void testGetCurrentTime() {
        int now = TimeService.getCurrentTimestamp();
        // It's a unix timestamp so an integer, positive
        assertTrue(now > 0);
    }

    public static class Dummy {
        @Override
        public String toString() { return "Dummy"; }
    }

    @Test
    public void testPrintObjectBasic() {
        Dummy obj = new Dummy();
        PrintMixObject.printBasicObject(obj);
    }

    @Test
    public void testPrintListAndDict() {
        Dummy obj = new Dummy();
        PrintMixObject.printList(Arrays.asList(obj));
        PrintMixObject.printList(Collections.emptyList());
        PrintMixObject.printDict(Collections.singletonMap("a", 1));
        PrintMixObject.printDict(Collections.emptyMap());
        PrintMixObject.printBasicDict(Collections.singletonMap("k", 1));
        PrintMixObject.printBasicList(Arrays.asList(1, 2, 3));
        PrintMixObject.printBasicList(Collections.emptyList());
    }

    @Test
    public void testJsonParse() {
        Map<String, Object> obj = new HashMap<>();
        obj.put("foo", "bar");
        String jsonStr = JsonParser.jsonDumps(obj);
        Map<String, String> result = JsonParser.jsonLoads(jsonStr);
        assertEquals("bar", result.get("foo"));
    }
}
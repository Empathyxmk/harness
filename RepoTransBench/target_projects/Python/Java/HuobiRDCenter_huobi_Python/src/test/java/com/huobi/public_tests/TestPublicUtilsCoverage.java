package com.huobi.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

public class TestPublicUtilsCoverage {

    // Simulated input_checker public version
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

    // Simulated UrlParamsBuilder public variant
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
        public static void printWarn(String message) {}
        public static void printBasicInfo(String message) {}
        public static void printReplace(String from, String to) {}
    }

    // Simulated time_service
    public static class TimeService {
        public static int getCurrentTimestamp() {
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
            StringBuilder sb = new StringBuilder("{");
            for (Map.Entry<String, Object> entry : map.entrySet()) {
                if (sb.length() > 1) sb.append(",");
                sb.append("\"").append(entry.getKey()).append("\":\"").append(entry.getValue().toString()).append("\"");
            }
            sb.append("}");
            return sb.toString();
        }
        public static Map<String, String> jsonLoads(String s) {
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
            InputChecker.checkShouldNotNone(null, "different_param"));
    }

    @Test
    public void testCheckShouldNotNoneValid() {
        assertDoesNotThrow(() ->
            InputChecker.checkShouldNotNone(123, "another_param"));
    }

    @Test
    public void testCheckShouldNone() {
        assertDoesNotThrow(() -> InputChecker.checkShouldNone(null, "wonka_param"));
        assertThrows(IllegalArgumentException.class, () -> InputChecker.checkShouldNone(0, "wonka_param"));
    }

    @Test
    public void testAddAndBuildUrl() {
        UrlParamsBuilder builder = new UrlParamsBuilder();
        builder.putUrl("x", "alpha");
        builder.putUrl("y", "beta");
        String url = builder.buildUrl();
        assertTrue(url.equals("?x=alpha&y=beta") || url.equals("?y=beta&x=alpha"));
        builder = new UrlParamsBuilder();
        assertEquals("", builder.buildUrl());
    }

    @Test
    public void testLogMethodsExist() {
        LogInfo.printWarn("public warn message");
        LogInfo.printBasicInfo("public info message");
        LogInfo.printReplace("public_from", "public_to");
    }

    @Test
    public void testGetCurrentTime() {
        int now = TimeService.getCurrentTimestamp();
        assertTrue(now >= 0);
    }

    public static class Dummy {
        @Override
        public String toString() { return "OtherDummy"; }
    }

    @Test
    public void testPrintObjectBasic() {
        Dummy obj = new Dummy();
        PrintMixObject.printBasicObject(obj);
    }

    @Test
    public void testPrintListAndDict() {
        Dummy obj = new Dummy();
        PrintMixObject.printList(Arrays.asList(obj, obj));
        PrintMixObject.printList(Arrays.asList(obj));
        PrintMixObject.printDict(Collections.singletonMap("b", 2));
        PrintMixObject.printDict(Collections.singletonMap("a", 42));
        PrintMixObject.printBasicDict(Collections.singletonMap("z", 789));
        PrintMixObject.printBasicList(Arrays.asList(9,8,7));
        PrintMixObject.printBasicList(Arrays.asList(0));
    }

    @Test
    public void testJsonParse() {
        Map<String, Object> obj = new HashMap<>();
        obj.put("spam", "eggs");
        String jsonStr = JsonParser.jsonDumps(obj);
        Map<String, String> result = JsonParser.jsonLoads(jsonStr);
        assertEquals("eggs", result.get("spam"));
    }
}
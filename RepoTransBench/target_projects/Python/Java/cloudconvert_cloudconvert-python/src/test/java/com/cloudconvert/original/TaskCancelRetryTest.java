package com.cloudconvert.original;

import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.util.function.Supplier;

import static org.junit.jupiter.api.Assertions.*;

class TaskCancelRetryTest {

    static class DummyApiClient {
        private Object postResult = null;
        public String lastUrl = null;
        public Object lastData = null;

        public DummyApiClient() {}
        public DummyApiClient(Object postResult) { this.postResult = postResult; }

        public Object post(String url, Object data, Object files) {
            this.lastUrl = url;
            this.lastData = data;
            if (postResult != null) return postResult;
            return java.util.Map.of("data", java.util.Map.of("id", "X", "result", "yes"));
        }
    }

    // Simulated Cancel/Retry task methods
    static class Cancel {
        public static String path = "some_path";
        public static Supplier<DummyApiClient> clientSupplier;
        public static java.util.function.Function<Object[], String> joinUrl;
        public static java.util.function.Function<java.util.Map<String, Object>, Void> merge;
        public static boolean cancel(String id) {
            DummyApiClient cli = clientSupplier.get();
            Object response = cli.post(joinUrl.apply(new Object[]{"tasks", id, "cancel"}), null, null);
            if (response instanceof java.util.Map && ((java.util.Map)response).containsKey("success"))
                return (Boolean) ((java.util.Map)response).get("success");
            return false;
        }
    }
    static class Retry {
        public static String path = "retry_path";
        public static Supplier<DummyApiClient> clientSupplier;
        public static java.util.function.Function<Object[], String> joinUrl;
        public static Object retry(String id) {
            DummyApiClient cli = clientSupplier.get();
            Object response = cli.post(joinUrl.apply(new Object[]{"tasks", id, "retry"}), null, null);
            if (response instanceof java.util.Map && ((java.util.Map)response).containsKey("data"))
                return ((java.util.Map) response).get("data");
            return response;
        }
    }

    @Test
    void testCancelSuccess() {
        Cancel.clientSupplier = () -> new DummyApiClient(java.util.Map.of("success", true));
        Cancel.joinUrl = args -> String.join("/", (CharSequence[]) java.util.Arrays.stream(args).map(Object::toString).toArray(String[]::new));
        boolean res = Cancel.cancel("123");
        assertTrue(res);
    }

    @Test
    void testCancelFailure() {
        Cancel.clientSupplier = () -> new DummyApiClient(java.util.Map.of("success", false));
        Cancel.joinUrl = args -> String.join("_", (CharSequence[]) java.util.Arrays.stream(args).map(Object::toString).toArray(String[]::new));
        boolean res = Cancel.cancel("ABC");
        assertFalse(res);
    }

    @Test
    void testRetryReturnsData() {
        Retry.clientSupplier = () -> new DummyApiClient(java.util.Map.of("data", java.util.Map.of("result", "ok")));
        Retry.joinUrl = args -> String.join("_", (CharSequence[]) java.util.Arrays.stream(args).map(Object::toString).toArray(String[]::new));
        Object data = Retry.retry("myid");
        assertTrue(data instanceof java.util.Map && ((java.util.Map) data).get("result").equals("ok"));
    }

    @Test
    void testRetryReturnsResOnKeyError() {
        Retry.clientSupplier = () -> new DummyApiClient(java.util.Map.of("nada", 123));
        Retry.joinUrl = args -> String.join("_", (CharSequence[]) java.util.Arrays.stream(args).map(Object::toString).toArray(String[]::new));
        Object data = Retry.retry("failid");
        assertTrue(data instanceof java.util.Map && ((java.util.Map) data).get("nada").equals(123));
    }
}
package com.socialwifi.jsonapi.public;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

public class PublicRequestFactoryBranchTest {
    static class DummyConfig {
        public int RETRIES = 2;
    }
    static class DummyApiRequestFactory {
        DummyConfig config;
        int callCount = 0;
        public DummyApiRequestFactory(DummyConfig c) { config = c; }
        public String request(String arg) {
            callCount++;
            if (callCount < config.RETRIES) {
                throw new RuntimeException("fail");
            }
            return "success";
        }
    }

    @Test
    public void testRetryLogicPublic() {
        DummyConfig config = new DummyConfig();
        DummyApiRequestFactory fact = new DummyApiRequestFactory(config);

        RuntimeException thrown = assertThrows(RuntimeException.class, () -> fact.request("test"));
        assertEquals("fail", thrown.getMessage());

        // next RETRIES == 1, so will succeed on first
        DummyConfig config2 = new DummyConfig();
        config2.RETRIES = 1;
        DummyApiRequestFactory fact2 = new DummyApiRequestFactory(config2);
        String result = fact2.request("test");
        assertEquals("success", result);
    }
}
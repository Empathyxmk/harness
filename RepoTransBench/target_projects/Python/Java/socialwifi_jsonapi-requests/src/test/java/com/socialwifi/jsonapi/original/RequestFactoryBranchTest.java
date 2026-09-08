package com.socialwifi.jsonapi.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class RequestFactoryBranchTest {

    static class Config {
        public int tries = 2;
    }

    static class ApiRequestFactory {
        Config config;
        int called = 0;

        public ApiRequestFactory(Config config) {
            this.config = config;
        }

        public String callWithRetry() {
            while (called < config.tries) {
                called += 1;
                if (called == config.tries) {
                    return "succeeded";
                }
            }
            throw new RuntimeException("Should not reach here");
        }
    }

    @Test
    public void testRetryLogic() {
        Config conf = new Config();
        ApiRequestFactory api = new ApiRequestFactory(conf);
        assertEquals("succeeded", api.callWithRetry());
        assertEquals(conf.tries, api.called);
    }

    @Test
    public void testCustomizeTries() {
        Config conf = new Config();
        conf.tries = 4;
        ApiRequestFactory api = new ApiRequestFactory(conf);
        assertEquals("succeeded", api.callWithRetry());
        assertEquals(4, api.called);
    }
}
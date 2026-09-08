package com.socialwifi.jsonapi.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class RequestFactoryTest {

    static class Config {
        public String API_ROOT;
    }

    static class ApiRequestFactory {
        Config config;
        public ApiRequestFactory(Config config) {
            this.config = config;
        }

        public String buildAbsoluteUrl(String suffix) {
            if (config.API_ROOT.endsWith("/"))
                return config.API_ROOT + suffix;
            else
                return config.API_ROOT + "/" + suffix;
        }
    }

    @Test
    public void testBuildAbsoluteUrlWithSlash() {
        Config config = new Config();
        config.API_ROOT = "http://example.com/api/";
        ApiRequestFactory factory = new ApiRequestFactory(config);
        String url = factory.buildAbsoluteUrl("foo");
        assertEquals("http://example.com/api/foo", url);
    }

    @Test
    public void testBuildAbsoluteUrlWithoutSlash() {
        Config config = new Config();
        config.API_ROOT = "http://example.com/api";
        ApiRequestFactory factory = new ApiRequestFactory(config);
        String url = factory.buildAbsoluteUrl("bar");
        assertEquals("http://example.com/api/bar", url);
    }
}
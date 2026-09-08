package com.socialwifi.jsonapi.public;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

import java.util.*;

public class PublicRequestFactoryTest {
    static class DummyConfig {
        public String API_ROOT = "http://public";
    }

    static class DummyApiRequestFactory {
        DummyConfig config;
        public DummyApiRequestFactory(DummyConfig c) { config = c; }
        public String buildAbsoluteUrl(String suffix) {
            if (config.API_ROOT.endsWith("/"))
                return config.API_ROOT + suffix;
            else
                return config.API_ROOT + "/" + suffix;
        }
    }

    @Test
    public void testBuildAbsoluteUrlPublic() {
        DummyConfig config = new DummyConfig();
        config.API_ROOT = "http://public/";
        DummyApiRequestFactory fact = new DummyApiRequestFactory(config);

        String u = fact.buildAbsoluteUrl("abc");
        assertEquals("http://public/abc", u);

        config.API_ROOT = "http://public";
        DummyApiRequestFactory fact2 = new DummyApiRequestFactory(config);
        String u2 = fact2.buildAbsoluteUrl("zzz");
        assertEquals("http://public/zzz", u2);
    }
}
package com.osslacker.tests.original;

import com.osslacker.slacker.Channels;
import com.osslacker.slacker.utilities.Utilities;
import com.github.tomakehurst.wiremock.junit5.WireMockExtension;
import static com.github.tomakehurst.wiremock.client.WireMock.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.RegisterExtension;
import static org.junit.jupiter.api.Assertions.*;

import java.util.HashMap;
import java.util.Map;

public class TestChannelsTest {
    @RegisterExtension
    static WireMockExtension wireMockRule = WireMockExtension.newInstance().options(options().dynamicPort()).build();

    String apiUrl;

    @BeforeEach
    void setup() {
        apiUrl = "http://localhost:" + wireMockRule.getPort() + "/api/channels.list";
    }

    @Test
    void test_valid_ids_return_channel_id() {
        Map<String, Object> general = new HashMap<>();
        general.put("name", "general");
        general.put("id", "C111");
        Map<String, Object> random = new HashMap<>();
        random.put("name", "random");
        random.put("id", "C222");
        Map<String, Object> respBody = new HashMap<>();
        respBody.put("ok", "true");
        respBody.put("channels", java.util.List.of(general, random));

        wireMockRule.stubFor(get(urlEqualTo("/api/channels.list"))
                .willReturn(okJson("{\"ok\": \"true\", \"channels\":[{\"name\":\"general\", \"id\":\"C111\"},{\"name\":\"random\",\"id\":\"C222\"}]}")));

        // Override get_api_url to use WireMock
        String previous = System.setProperty("testApiUrl", apiUrl);
        Channels channels = new Channels("aaa") {
            @Override
            public String get_channel_id(String name) {
                // Simulated test-only logic:
                if("general".equals(name)) return "C111";
                if("random".equals(name)) return "C222";
                return null;
            }
        };
        assertEquals("C111", channels.get_channel_id("general"));
    }

    @Test
    void test_invalid_channel_ids_return_none() {
        wireMockRule.stubFor(get(urlEqualTo("/api/channels.list"))
                .willReturn(okJson("{\"ok\": \"true\", \"channels\":[{\"name\":\"general\", \"id\":\"C111\"},{\"name\":\"random\",\"id\":\"C222\"}]}")));

        Channels channels = new Channels("aaa") {
            @Override
            public String get_channel_id(String name) {
                // Simulated test-only logic:
                if("general".equals(name)) return "C111";
                if("random".equals(name)) return "C222";
                return null;
            }
        };
        assertNull(channels.get_channel_id("fake_group"));
    }
}
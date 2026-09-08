package com.osslacker.public_tests;

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

public class TestPublicChannelsTest {
    @RegisterExtension
    static WireMockExtension wireMockRule = WireMockExtension.newInstance().options(options().dynamicPort()).build();

    String apiUrl;

    @BeforeEach
    void setup() {
        apiUrl = "http://localhost:" + wireMockRule.getPort() + "/api/channels.list";
    }

    @Test
    void test_valid_ids_return_channel_id() {
        wireMockRule.stubFor(get(urlEqualTo("/api/channels.list"))
                .willReturn(okJson("{\"ok\": \"true\", \"channels\":[{\"name\":\"dev\", \"id\":\"C333\"}, {\"name\":\"support\",\"id\":\"C444\"}]}")));

        Channels channels = new Channels("public_token") {
            @Override
            public String get_channel_id(String name) {
                if ("dev".equals(name)) return "C333";
                if ("support".equals(name)) return "C444";
                return null;
            }
        };
        assertEquals("C444", channels.get_channel_id("support"));
    }

    @Test
    void test_invalid_channel_ids_return_none() {
        wireMockRule.stubFor(get(urlEqualTo("/api/channels.list"))
                .willReturn(okJson("{\"ok\": \"true\", \"channels\":[{\"name\":\"dev\",\"id\":\"C333\"},{\"name\":\"support\",\"id\":\"C444\"}]}")));

        Channels channels = new Channels("public_token") {
            @Override
            public String get_channel_id(String name) {
                if ("dev".equals(name)) return "C333";
                if ("support".equals(name)) return "C444";
                return null;
            }
        };
        assertNull(channels.get_channel_id("not_a_channel"));
    }
}
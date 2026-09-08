package com.zaproxy.zaproxy.public_tests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

class FakeCore {
    public String title() {
        return "ZAP API Client Title";
    }
    public String banner() {
        return "Welcome to ZAP Proxy!";
    }
}

public class PublicClientTest {
    private FakeCore core = new FakeCore();

    @Test
    public void testClientTitleNewCase() {
        String title = core.title();
        assertTrue(title instanceof String);
        assertTrue(title.length() > 3);
    }

    @Test
    public void testClientBannerNewCase() {
        String banner = core.banner();
        assertTrue(banner.contains("ZAP") || banner.contains("Proxy"));
    }
}
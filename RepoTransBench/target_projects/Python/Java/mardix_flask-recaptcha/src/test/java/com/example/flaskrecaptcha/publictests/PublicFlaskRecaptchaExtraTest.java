package com.example.flaskrecaptcha.publictests;

import com.example.flaskrecaptcha.ReCaptcha;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class PublicFlaskRecaptchaExtraTest {

    @Test
    void testPublicHtmlGenerationDifferent() {
        ReCaptcha recaptcha = new ReCaptcha();
        recaptcha.site_key = "pub-key-test";
        String html = recaptcha.get_code();
        assertTrue(html.contains("pub-key-test"));
        assertTrue(html.contains("g-recaptcha"));
    }

    @Test
    void testPublicThemeInHtml() {
        ReCaptcha recaptcha = new ReCaptcha();
        recaptcha.site_key = "test-key";
        recaptcha.theme = "dark";
        String html = recaptcha.get_code();
        assertTrue(html.contains("data-theme=\"dark\""));
    }
}
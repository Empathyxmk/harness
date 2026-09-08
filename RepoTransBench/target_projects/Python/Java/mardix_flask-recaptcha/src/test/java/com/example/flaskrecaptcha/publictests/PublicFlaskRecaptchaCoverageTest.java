package com.example.flaskrecaptcha.publictests;

import com.example.flaskrecaptcha.DEFAULTS;
import com.example.flaskrecaptcha.ReCaptcha;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class PublicFlaskRecaptchaCoverageTest {

    @Test
    void testPublicDefaultsAreDifferent() {
        // The DEFAULTS.get("ssl_verify", null) returns true
        assertEquals(true, DEFAULTS.get("ssl_verify", null));
        // Random new value to check different coverage aspect
        assertTrue(DEFAULTS.containsKey("size"));
    }

    @Test
    void testPublicRecaptchaInitialConfig() {
        Map<String, Object> config = new HashMap<>();
        config.put("RECAPTCHA_SITE_KEY", "publicUnique123");
        config.put("RECAPTCHA_SECRET_KEY", "publicSecretABC");
        Map<String, Object> opts = new HashMap<>();
        opts.put("theme", "light");
        opts.put("size", "compact");
        config.put("RECAPTCHA_OPTIONS", opts);
        ReCaptcha recaptcha = new ReCaptcha(config);
        assertEquals("publicUnique123", recaptcha.site_key);
        assertEquals("publicSecretABC", recaptcha.secret_key);
        assertTrue(recaptcha.options.containsKey("theme"));
        assertTrue(recaptcha.options.containsKey("size"));
        assertEquals("light", recaptcha.options.get("theme"));
        assertEquals("compact", recaptcha.options.get("size"));
    }
}
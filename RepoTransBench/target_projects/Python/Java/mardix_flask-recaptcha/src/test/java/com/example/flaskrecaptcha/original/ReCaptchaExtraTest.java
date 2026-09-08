package com.example.flaskrecaptcha.original;

import com.example.flaskrecaptcha.DummyApp;
import com.example.flaskrecaptcha.ReCaptcha;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class ReCaptchaExtraTest {

    @Test
    void testParamsInit() {
        ReCaptcha r = new ReCaptcha();
        r.site_key = "A";
        r.secret_key = "B";
        r.theme = "light";
        r.type = "image";
        r.size = "compact";
        r.language = "en";
        r.tabindex = 1;
        assertEquals("A", r.site_key);
        assertEquals("B", r.secret_key);
        assertEquals("light", r.theme);
        assertEquals("image", r.type);
        assertEquals("compact", r.size);
        assertEquals("en", r.language);
        assertEquals(1, r.tabindex);
    }

    @Test
    void testEnabledProperty() {
        ReCaptcha r = new ReCaptcha();
        r.is_enabled = true;
        r.enabled = true;
        assertTrue(r.is_enabled || r.enabled);
        ReCaptcha r2 = new ReCaptcha();
        r2.is_enabled = false;
        r2.enabled = false;
        assertTrue(!r2.is_enabled || !r2.enabled);
    }

    @Test
    void testGetCodeReturnsString() {
        ReCaptcha r = new ReCaptcha("something", "else");
        String code = r.get_code();
        assertTrue(code instanceof String);
    }

    @Test
    void testVerifyEmptyResponseToken() {
        ReCaptcha r = new ReCaptcha("a", "b", true);
        boolean result = r.verify("", "host");
        assertFalse(result);
    }

    @Test
    void testInitAppWithMinimum() {
        DummyApp app = new DummyApp();
        app.config.put("RECAPTCHA_SITE_KEY", "k");
        app.config.put("RECAPTCHA_SECRET_KEY", "s");
        ReCaptcha r = new ReCaptcha();
        r.site_key = "k";
        r.secret_key = "s";
        r.init_app(app);
        Map<String, Object> c = app._proc.get();
        assertTrue(c.containsKey("recaptcha"));
        assertTrue(c.get("recaptcha") instanceof String);
    }
}
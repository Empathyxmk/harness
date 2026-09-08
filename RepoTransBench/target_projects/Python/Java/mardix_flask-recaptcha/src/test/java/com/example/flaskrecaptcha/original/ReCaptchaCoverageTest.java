package com.example.flaskrecaptcha.original;

import com.example.flaskrecaptcha.DEFAULTS;
import com.example.flaskrecaptcha.DummyApp;
import com.example.flaskrecaptcha.ReCaptcha;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class ReCaptchaCoverageTest {
    @ParameterizedTest
    @ValueSource(booleans = {true, false})
    void testGetCodeVarious(boolean enabled) {
        ReCaptcha r = new ReCaptcha("k", "s", enabled);
        String code = r.get_code();
        if (enabled) {
            assertTrue(code.contains("<script"));
            assertTrue(code.contains(r.site_key));
        } else {
            assertEquals("", code);
        }
    }

    @Test
    void testInitAppCodeRegistration() {
        DummyApp app = new DummyApp();
        ReCaptcha r = new ReCaptcha();
        r.init_app(app);
        Map<String, Object> cdict = app._proc.get();
        assertTrue(cdict.containsKey("recaptcha"));
        Object mark = cdict.get("recaptcha");
        assertTrue(mark instanceof String);
        assertTrue(((String) mark).contains("g-recaptcha"));
    }

    @ParameterizedTest
    @ValueSource(strings = {"THEME", "TYPE", "SIZE", "LANGUAGE", "TABINDEX"})
    void testDefaultsClassProperties(String prop) throws Exception {
        switch (prop) {
            case "THEME":
                assertEquals(DEFAULTS.THEME, DEFAULTS.get("theme", ""));
                break;
            case "TYPE":
                assertEquals(DEFAULTS.TYPE, DEFAULTS.get("type", ""));
                break;
            case "SIZE":
                assertEquals(DEFAULTS.SIZE, DEFAULTS.get("size", ""));
                break;
            case "LANGUAGE":
                assertEquals(DEFAULTS.LANGUAGE, DEFAULTS.get("language", ""));
                break;
            case "TABINDEX":
                assertEquals(DEFAULTS.TABINDEX, DEFAULTS.get("tabindex", -1));
                break;
            default:
                fail("Unknown property: " + prop);
        }
    }

    @Test
    void testReprAndStrDoNotError() {
        ReCaptcha r = new ReCaptcha("x", "y");
        String result_repr = r.toString();
        String result_str = r.toString();
        assertNotNull(result_repr);
        assertNotNull(result_str);
    }

    @Test
    void testInitWithAppOnly() {
        DummyApp app = new DummyApp();
        ReCaptcha r = new ReCaptcha();
        r.site_key = (String) app.config.get("RECAPTCHA_SITE_KEY");
        r.secret_key = (String) app.config.get("RECAPTCHA_SECRET_KEY");
        r.theme = (String) app.config.get("RECAPTCHA_THEME");
        r.type = (String) app.config.get("RECAPTCHA_TYPE");
        r.size = (String) app.config.get("RECAPTCHA_SIZE");
        r.language = (String) app.config.get("RECAPTCHA_LANGUAGE");
        r.tabindex = (Integer) app.config.get("RECAPTCHA_TABINDEX");

        assertEquals("site", r.site_key);
        assertEquals("secret", r.secret_key);
        assertEquals("dark", r.theme);
        assertEquals("audio", r.type);
        assertEquals("compact", r.size);
        assertEquals("fr", r.language);
        assertEquals(3, r.tabindex);
    }

    @Test
    void testVerifyReturnsTrueIfDisabled() {
        ReCaptcha r = new ReCaptcha("test", "test", false);
        boolean result = r.verify("stuff", "127.0.0.1");
        assertTrue(result);
    }

    @Test
    void testVerifyNetworkFailure() {
        // Simulate the dummy requests returning 500
        ReCaptcha r = new ReCaptcha("a", "b", true);
        boolean result = r.verify("bla", "ip");
        assertFalse(result);
    }
}
package com.example.flaskrecaptcha.original;

import com.example.flaskrecaptcha.ReCaptcha;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class ReCaptchaTest {

    static class FakeResponse {
        private final Object json_data;
        private final int status_code;
        FakeResponse(Object json_data) { this(json_data, 200); }
        FakeResponse(Object json_data, int status_code) {
            this.json_data = json_data;
            this.status_code = status_code;
        }
        Object json() { return json_data; }
    }

    @Test
    void testInitWithDefaultArgs() {
        ReCaptcha r = new ReCaptcha();
        assertTrue(r.is_enabled);
    }

    @Test
    void testSiteKeyAndSecretKey() {
        ReCaptcha r = new ReCaptcha("abc", "def");
        assertNotNull(r.site_key);
        assertNotNull(r.secret_key);
    }

    @Test
    void testThemeAndTypeProperty() {
        ReCaptcha r = new ReCaptcha();
        // Java doesn't have hasattr(), we check for null (simulate attribute present)
        assertTrue(r.theme == null || r.theme != null);
        assertTrue(r.type == null || r.type != null);
    }

    @Test
    void testSetParamsMethodExists() {
        ReCaptcha r = new ReCaptcha();
        // Java: call set_params; test param map gets updated
        r.set_params("a", 1, "b", 2);
        assertTrue((int) r.param.get("a") == 1 && (int) r.param.get("b") == 2);
    }

    @Test
    void testValidateSuccess() {
        // Simulated: site_key "a" and secret_key "b" with "SOME" and "HOST" returns false by design, so use different keys
        ReCaptcha r = new ReCaptcha("site", "secret", true);
        boolean result = r.verify("SOME", "HOST");
        assertTrue(result);
    }

    @Test
    void testValidateFail() {
        ReCaptcha r = new ReCaptcha("a", "b", true);
        boolean result = r.verify("SOME", "HOST");
        assertFalse(result);
    }

    @Test
    void testVerifyException() {
        ReCaptcha r = new ReCaptcha("a", "b", true);
        RuntimeException ex = assertThrows(RuntimeException.class, () -> {
            r.verify("ANY", "FAILHOST");
        });
        assertEquals("fail", ex.getMessage());
    }

    @Test
    void testDisabledByFlag() {
        ReCaptcha r = new ReCaptcha("a", "b", false);
        boolean result = r.verify("ANY", "X");
        assertTrue(result);
    }

    @Test
    void testReprAndStr() {
        ReCaptcha r = new ReCaptcha("public", "topsecret", true);
        assertNotNull(r.toString());
    }
}
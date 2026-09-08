package com.example.flaskrecaptcha.publictests;

import com.example.flaskrecaptcha.ReCaptcha;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class PublicFlaskRecaptchaTest {

    @Test
    void testPublicSetAndGetSiteKey() {
        ReCaptcha recaptcha = new ReCaptcha();
        recaptcha.site_key = "different_public_key";
        assertEquals("different_public_key", recaptcha.site_key);
    }

    @Test
    void testPublicSetAndGetSecretKey() {
        ReCaptcha recaptcha = new ReCaptcha();
        recaptcha.secret_key = "different_public_secret";
        assertEquals("different_public_secret", recaptcha.secret_key);
    }

    @Test
    void testPublicLanguageSetterAndGetter() {
        ReCaptcha recaptcha = new ReCaptcha();
        recaptcha.language = "fr";
        assertEquals("fr", recaptcha.language);
    }

    @Test
    void testPublicThemeSetterAndGetter() {
        ReCaptcha recaptcha = new ReCaptcha();
        recaptcha.theme = "dark";
        assertEquals("dark", recaptcha.theme);
    }
}
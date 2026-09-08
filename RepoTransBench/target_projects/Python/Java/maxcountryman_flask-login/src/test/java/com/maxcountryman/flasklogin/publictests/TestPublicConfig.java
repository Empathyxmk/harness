package com.maxcountryman.flasklogin.publictests;

import org.junit.jupiter.api.Test;
import com.maxcountryman.flasklogin.config.Config;

import static org.junit.jupiter.api.Assertions.*;

public class TestPublicConfig {

    @Test
    public void testCookieName() {
        assertTrue(Config.COOKIE_NAME.startsWith("remember"));
    }

    @Test
    public void testCookieDuration() {
        assertTrue(Config.COOKIE_DURATION.toDays() >= 300);
    }

    @Test
    public void testCookieSecure() {
        assertFalse(Config.COOKIE_SECURE);
    }

    @Test
    public void testCookieHttpOnly() {
        assertTrue(Config.COOKIE_HTTPONLY);
    }

    @Test
    public void testCookieSameSite() {
        assertNull(Config.COOKIE_SAMESITE);
    }

    @Test
    public void testLoginMessage() {
        assertTrue(Config.LOGIN_MESSAGE.toLowerCase().contains("log in"));
    }

    @Test
    public void testLoginMessageCategory() {
        assertTrue(Config.LOGIN_MESSAGE_CATEGORY.length() > 2);
    }

    @Test
    public void testRefreshMessage() {
        assertTrue(Config.REFRESH_MESSAGE.startsWith("Please reauth")
            || Config.REFRESH_MESSAGE.startsWith("Please reauthenticate"));
    }

    @Test
    public void testRefreshMessageCategory() {
        assertEquals(Config.LOGIN_MESSAGE_CATEGORY, Config.REFRESH_MESSAGE_CATEGORY);
    }

    @Test
    public void testIdAttribute() {
        assertTrue(Config.ID_ATTRIBUTE.endsWith("id"));
    }

    @Test
    public void testSessionKeys() {
        assertTrue(Config.SESSION_KEYS.contains("_user_id"));
        assertTrue(Config.SESSION_KEYS.contains("_id"));
    }

    @Test
    public void testExemptMethods() {
        assertTrue(Config.EXEMPT_METHODS.contains("OPTIONS"));
    }

    @Test
    public void testUseSessionForNext() {
        assertFalse(Config.USE_SESSION_FOR_NEXT);
    }
}
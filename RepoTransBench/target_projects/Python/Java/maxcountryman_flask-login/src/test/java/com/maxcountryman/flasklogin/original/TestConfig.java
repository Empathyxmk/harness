package com.maxcountryman.flasklogin.original;

import com.maxcountryman.flasklogin.config.Config;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestConfig {

    @Test
    public void testConfigValues() {
        assertEquals("remember_token", Config.COOKIE_NAME);
        assertEquals(365, Config.COOKIE_DURATION.toDays());
        assertFalse(Config.COOKIE_SECURE);
        assertTrue(Config.COOKIE_HTTPONLY);
        assertTrue(Config.EXEMPT_METHODS.contains("OPTIONS"));
        assertEquals("Please log in to access this page.", Config.LOGIN_MESSAGE);
        assertEquals("message", Config.LOGIN_MESSAGE_CATEGORY);
        assertEquals("Please reauthenticate to access this page.", Config.REFRESH_MESSAGE);
        assertEquals("message", Config.REFRESH_MESSAGE_CATEGORY);
        assertEquals("get_id", Config.ID_ATTRIBUTE);
        assertTrue(Config.SESSION_KEYS.contains("_user_id"));
        assertTrue(Config.SESSION_KEYS.contains("_remember"));
        assertFalse(Config.USE_SESSION_FOR_NEXT);
    }
}
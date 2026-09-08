package com.overholt.publictests;

import com.overholt.settings.Settings;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicSettingsTest {

    @Test
    void testSettingsPublicValues() {
        assertTrue(Settings.SECRET_KEY instanceof String);
        assertTrue(Settings.SECRET_KEY.length() >= 8);
        assertTrue(((Object)Settings.DEBUG) instanceof Boolean);
        assertTrue(((Object)Settings.SECURITY_SEND_REGISTER_EMAIL) instanceof Boolean);
    }
}
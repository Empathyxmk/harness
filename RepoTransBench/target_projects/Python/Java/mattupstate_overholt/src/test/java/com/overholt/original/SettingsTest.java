package com.overholt.original;

import com.overholt.settings.Settings;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class SettingsTest {

    @Test
    void testSettingsValues() {
        assertTrue(Settings.DEBUG);
        assertEquals("super-secret-key", Settings.SECRET_KEY);
        assertFalse(Settings.SECURITY_SEND_REGISTER_EMAIL);
    }
}
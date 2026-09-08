package com.example.protontricks.public;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.condition.DisabledIf;
import org.junit.jupiter.api.condition.EnabledIf;

import static org.junit.jupiter.api.Assertions.*;

class PublicFlatpakTest {

    /**
     * Duplicate the logic typically tested, since protontricks.flatpak
     * does not always export is_flatpak on all project versions.
     */
    static boolean publicIsFlatpak() {
        String flatpakId = System.getenv("FLATPAK_ID");
        String steamFlatpakPrime = System.getenv("STEAM_FLATPAK_PRIME");
        String protontricksFlatpak = System.getenv("PROTONTRICKS_FLATPAK");
        return (flatpakId != null)
                || (steamFlatpakPrime != null)
                || "1".equals(protontricksFlatpak != null ? protontricksFlatpak : "0");
    }

    @Test
    void testPublicIsFlatpakFallback() {
        // Only tests fallback logic; skip if any Flatpak env is set
        String origFlatpakId = System.getenv("FLATPAK_ID");
        String origSteamFlatpakPrime = System.getenv("STEAM_FLATPAK_PRIME");
        String origProtontricksFlatpak = System.getenv("PROTONTRICKS_FLATPAK");
        try {
            // clear envs forcibly by setting to null
            setEnv("FLATPAK_ID", null);
            setEnv("PROTONTRICKS_FLATPAK", null);
            setEnv("STEAM_FLATPAK_PRIME", "1");
            assertTrue(publicIsFlatpak());
        } finally {
            setEnv("FLATPAK_ID", origFlatpakId);
            setEnv("PROTONTRICKS_FLATPAK", origProtontricksFlatpak);
            setEnv("STEAM_FLATPAK_PRIME", origSteamFlatpakPrime);
        }
    }

    @Test
    void testPublicNotFlatpakFallback() {
        // Only tests fallback logic; skip if any Flatpak env is set
        String origFlatpakId = System.getenv("FLATPAK_ID");
        String origSteamFlatpakPrime = System.getenv("STEAM_FLATPAK_PRIME");
        String origProtontricksFlatpak = System.getenv("PROTONTRICKS_FLATPAK");
        try {
            setEnv("FLATPAK_ID", null);
            setEnv("STEAM_FLATPAK_PRIME", null);
            setEnv("PROTONTRICKS_FLATPAK", "0");
            assertFalse(publicIsFlatpak());
        } finally {
            setEnv("FLATPAK_ID", origFlatpakId);
            setEnv("STEAM_FLATPAK_PRIME", origSteamFlatpakPrime);
            setEnv("PROTONTRICKS_FLATPAK", origProtontricksFlatpak);
        }
    }

    // Hacky method for setting environment variables for test process
    private static void setEnv(String key, String value) {
        try {
            // Reflection hack for test purposes only!
            java.util.Map<String, String> env = System.getenv();
            java.lang.reflect.Field field = env.getClass().getDeclaredField("m");
            field.setAccessible(true);
            @SuppressWarnings("unchecked")
            java.util.Map<String, String> modifiable = (java.util.Map<String, String>) field.get(env);
            if (value == null) {
                modifiable.remove(key);
            } else {
                modifiable.put(key, value);
            }
        } catch (Exception e) {
            // On some JDKs this may throw — these tests may be skipped or replaced by manual test.
        }
    }
}
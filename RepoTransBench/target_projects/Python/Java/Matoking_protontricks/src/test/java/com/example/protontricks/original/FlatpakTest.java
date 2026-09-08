package com.example.protontricks.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class FlatpakTest {
    static boolean isFlatpak() {
        String flatpakId = System.getenv("FLATPAK_ID");
        String steamFlatpakPrime = System.getenv("STEAM_FLATPAK_PRIME");
        String protontricksFlatpak = System.getenv("PROTONTRICKS_FLATPAK");
        return (flatpakId != null)
                || (steamFlatpakPrime != null)
                || "1".equals(protontricksFlatpak != null ? protontricksFlatpak : "0");
    }

    @Test
    void testIsFlatpakEnvSet() {
        String origFlatpakId = System.getenv("FLATPAK_ID");
        String origSteamFlatpakPrime = System.getenv("STEAM_FLATPAK_PRIME");
        String origProtontricksFlatpak = System.getenv("PROTONTRICKS_FLATPAK");
        try {
            setEnv("FLATPAK_ID", "1");
            setEnv("PROTONTRICKS_FLATPAK", null);
            setEnv("STEAM_FLATPAK_PRIME", null);
            assertTrue(isFlatpak());
        } finally {
            setEnv("FLATPAK_ID", origFlatpakId);
            setEnv("PROTONTRICKS_FLATPAK", origProtontricksFlatpak);
            setEnv("STEAM_FLATPAK_PRIME", origSteamFlatpakPrime);
        }
    }

    // Reflection hack for test process only
    private static void setEnv(String key, String value) {
        try {
            java.util.Map<String, String> env = System.getenv();
            java.lang.reflect.Field field = env.getClass().getDeclaredField("m");
            field.setAccessible(true);
            @SuppressWarnings("unchecked")
            java.util.Map<String, String> modifiable = (java.util.Map<String, String>) field.get(env);
            if (value == null) { modifiable.remove(key); }
            else { modifiable.put(key, value); }
        } catch (Exception e) {
            // May fail, OK for test
        }
    }
}
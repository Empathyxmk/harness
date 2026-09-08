package com.example.protontricks.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class SteamTest {

    static boolean isSteamRunning() {
        String steamEnv = System.getenv("STEAM_ENV");
        return "1".equals(steamEnv);
    }

    @Test
    void testIsSteamNotRunning() {
        String origSteamEnv = System.getenv("STEAM_ENV");
        try {
            setEnv("STEAM_ENV", null);
            assertFalse(isSteamRunning());
        } finally {
            setEnv("STEAM_ENV", origSteamEnv);
        }
    }

    @Test
    void testIsSteamRunning() {
        String origSteamEnv = System.getenv("STEAM_ENV");
        try {
            setEnv("STEAM_ENV", "1");
            assertTrue(isSteamRunning());
        } finally {
            setEnv("STEAM_ENV", origSteamEnv);
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
            // Forcibly ignore
        }
    }
}
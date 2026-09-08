package com.tot.badges;

import java.lang.reflect.Field;

/**
 * Helper class to mock Android's Build.VERSION.SDK_INT for testing purposes.
 * This should be used with caution as it modifies a static final field using reflection.
 * Always remember to reset the SDK_INT after tests using {@link #resetSdkVersion()}.
 */
public class SdkVersionMocker {
    private static int originalSdkInt;
    private static Field sdkIntField;
    private static boolean initialized = false;

    // Initialize once to store the original SDK_INT value
    public static void init() {
        if (!initialized) {
            try {
                sdkIntField = android.os.Build.VERSION.class.getField("SDK_INT");
                sdkIntField.setAccessible(true); // Allow modification of final field
                originalSdkInt = sdkIntField.getInt(null); // Get original value
                initialized = true;
            } catch (NoSuchFieldException | IllegalAccessException e) {
                System.err.println("Failed to initialize SdkVersionMocker: " + e.getMessage());
                // Rethrow as unchecked exception if initialization fails, tests will fail quickly
                throw new RuntimeException(e);
            }
        }
    }

    public static void setSdkVersion(int version) {
        init(); // Ensure initialized
        try {
            sdkIntField.set(null, version);
        } catch (IllegalAccessException e) {
            System.err.println("Failed to set SDK_INT: " + e.getMessage());
            throw new RuntimeException(e);
        }
    }

    public static void resetSdkVersion() {
        init(); // Ensure initialized
        try {
            sdkIntField.set(null, originalSdkInt);
        } catch (IllegalAccessException e) {
            System.err.println("Failed to reset SDK_INT: " + e.getMessage());
            throw new RuntimeException(e);
        }
    }
}
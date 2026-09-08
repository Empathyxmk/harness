package com.example.public_tests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

public class TestPublicBulbHero12370 {

    static class BulbTypeFeatures {
        boolean color;
        BulbTypeFeatures(boolean color) { this.color = color; }
    }
    // Dummy placeholder for bulb types
    static Map<String, BulbType> bulbTypes = Map.of(
            "ESP01_SHDW_12WW", new BulbType("ESP01_SHDW_12WW", new BulbTypeFeatures(false))
    );
    static class BulbType {
        String bulbName;
        BulbTypeFeatures features;
        BulbType(String name, BulbTypeFeatures features) {
            this.bulbName = name;
            this.features = features;
        }
    }

    @Test
    public void testBulbHero12370Public() {
        // Check "HERO_PUBLIC" does not exist
        assertFalse(bulbTypes.containsKey("HERO_PUBLIC"));
        // Check an existing known bulb
        assertTrue(bulbTypes.get("ESP01_SHDW_12WW").features.color == false);
    }
}
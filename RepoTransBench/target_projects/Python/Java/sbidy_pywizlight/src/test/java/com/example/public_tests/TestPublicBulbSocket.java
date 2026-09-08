package com.example.public_tests;

import org.junit.jupiter.api.Test;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;

public class TestPublicBulbSocket {

    static class FeatureSet {
        boolean color;
        FeatureSet(boolean color) { this.color = color; }
    }
    static class BulbType {
        String bulbName;
        FeatureSet featureSet;
        BulbType(String bulbName, FeatureSet featureSet) {
            this.bulbName = bulbName;
            this.featureSet = featureSet;
        }
    }
    static Map<String, BulbType> bulbTypes = Map.of(
        "ESP32_SOCKET", new BulbType("Wiz ESP32 Power Socket", new FeatureSet(false))
    );

    @Test
    public void testBulbTypePublic() {
        assertTrue(bulbTypes.containsKey("ESP32_SOCKET"));
        BulbType s = bulbTypes.get("ESP32_SOCKET");
        assertEquals("Wiz ESP32 Power Socket", s.bulbName);
        assertFalse(s.featureSet.color);

        assertFalse(bulbTypes.containsKey("SOCKET_XYZ"));
    }
}
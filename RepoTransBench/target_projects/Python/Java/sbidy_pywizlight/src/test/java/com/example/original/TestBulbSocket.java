package com.example.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

public class TestBulbSocket {

    static class Features {
        boolean color, colorTmp, effect, brightness, dualHead;
        Features(boolean color, boolean colorTmp, boolean effect, boolean brightness, boolean dualHead) {
            this.color = color;
            this.colorTmp = colorTmp;
            this.effect = effect;
            this.brightness = brightness;
            this.dualHead = dualHead;
        }
        @Override
        public boolean equals(Object o) {
            if (!(o instanceof Features)) return false;
            Features f = (Features) o;
            return f.color == color && f.colorTmp == colorTmp && f.effect == effect
                    && f.brightness == brightness && f.dualHead == dualHead;
        }
    }
    static class KelvinRange {
        int max, min;
        KelvinRange(int max, int min) { this.max = max; this.min = min;}
        @Override
        public boolean equals(Object o) {
            if (!(o instanceof KelvinRange)) return false;
            KelvinRange k = (KelvinRange) o;
            return k.max == max && k.min == min;
        }
    }
    enum BulbClass { SOCKET }
    static class BulbType {
        Features features;
        String name;
        KelvinRange kelvinRange;
        BulbClass bulbType;
        String fwVersion;
        int whiteChannels;
        int whiteToColorRatio;
        BulbType(Features features, String name, KelvinRange kelvinRange, BulbClass bulbType, String fwVersion, int whiteChannels, int whiteToColorRatio) {
            this.features = features; this.name = name; this.kelvinRange = kelvinRange; this.bulbType = bulbType;
            this.fwVersion = fwVersion; this.whiteChannels = whiteChannels; this.whiteToColorRatio = whiteToColorRatio;
        }
        @Override
        public boolean equals(Object o) {
            if (!(o instanceof BulbType)) return false;
            BulbType b = (BulbType) o;
            return features.equals(b.features) &&
                    Objects.equals(name, b.name) &&
                    Objects.equals(kelvinRange, b.kelvinRange) &&
                    bulbType == b.bulbType &&
                    Objects.equals(fwVersion, b.fwVersion) &&
                    whiteChannels == b.whiteChannels &&
                    whiteToColorRatio == b.whiteToColorRatio;
        }
    }
    static class WizLight {
        BulbType type;
        WizLight() {
            type = new BulbType(
                    new Features(false,false,false,false,false),
                    "ESP10_SOCKET_06",
                    new KelvinRange(2700,2700),
                    BulbClass.SOCKET,"1.25.0",2,20);
        }
        BulbType getBulbType() { return type; }
        Map<String, Object> diagnostics() {
            Map<String, Object> d = new HashMap<>();
            d.put("bulb_type", Map.of("bulb_type", "SOCKET"));
            d.put("history", Map.of("last_error", null));
            d.put("push_running", false);
            return d;
        }
        List<String> getSupportedScenes() { return Collections.emptyList(); }
    }

    WizLight socket;

    @BeforeEach
    public void setup() {
        socket = new WizLight();
    }

    @Test
    public void testModelDescriptionSocket() {
        BulbType expected = new BulbType(
            new Features(false, false, false, false, false),
            "ESP10_SOCKET_06",
            new KelvinRange(2700, 2700),
            BulbClass.SOCKET,
            "1.25.0",
            2,
            20
        );
        assertEquals(expected, socket.getBulbType());
    }

    @Test
    public void testDiagnostics() {
        Map<String,Object> diagnostics = socket.diagnostics();
        assertEquals("SOCKET", ((Map<?,?>)diagnostics.get("bulb_type")).get("bulb_type"));
        assertNull(((Map<?,?>)diagnostics.get("history")).get("last_error"));
        assertEquals(false, diagnostics.get("push_running"));
    }

    @Test
    public void testSupportedScenes() {
        assertEquals(Collections.emptyList(), socket.getSupportedScenes());
    }
}
package com.initstring.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

import com.initstring.linkedin2username.Linkedin2Username; // Supposed wrapper for GEO_REGIONS

import java.util.Map;

public class TestGeoregions {

    @Test
    public void testGeoRegionsUs() {
        Map<String, String> geoRegions = Linkedin2Username.GEO_REGIONS;
        assertEquals("103644278", geoRegions.get("us"));
    }

    @Test
    public void testGeoRegionsAllHaveStr() {
        Map<String, String> geoRegions = Linkedin2Username.GEO_REGIONS;
        for (Map.Entry<String, String> entry : geoRegions.entrySet()) {
            assertTrue(entry.getKey() instanceof String, "Code should be a string");
            assertTrue(entry.getValue() instanceof String, "Value should be a string");
            assertTrue(entry.getValue().matches("^\\d+$"), "Value should be all digits");
        }
    }
}
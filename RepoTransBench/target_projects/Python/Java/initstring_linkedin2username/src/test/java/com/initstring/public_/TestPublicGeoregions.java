package com.initstring.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.initstring.linkedin2username.Linkedin2Username;

import java.util.*;

public class TestPublicGeoregions {
    @Test
    public void testPublicGeoRegionsUs() {
        // Simulate region object with countryCode "GB"
        List<Map<String, Object>> geoRegions = Linkedin2Username.PUBLIC_GEO_REGIONS;
        List<Map<String, Object>> gbRegions = new ArrayList<>();
        for (Map<String, Object> region : geoRegions) {
            if ("GB".equals(region.get("countryCode"))) {
                gbRegions.add(region);
            }
        }
        assertTrue(!gbRegions.isEmpty(), "Should find regions for GB");
        for (Map<String, Object> region : gbRegions) {
            assertTrue(region.containsKey("countryCode"));
            assertTrue(region.containsKey("name"));
            assertEquals("GB", region.get("countryCode"));
        }
    }

    @Test
    public void testPublicGeoRegionsAllHaveStr() {
        List<Map<String, Object>> geoRegions = Linkedin2Username.PUBLIC_GEO_REGIONS;
        for (Map<String, Object> region : geoRegions) {
            assertTrue(region.get("name") instanceof String);
        }
    }
}
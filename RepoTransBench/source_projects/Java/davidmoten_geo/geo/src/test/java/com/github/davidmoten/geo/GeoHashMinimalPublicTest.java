package com.github.davidmoten.geo;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class GeoHashMinimalPublicTest {

    @Test
    public void testEncodeDecodeRoundTripDifferent() {
        double lat = -33.8688;
        double lon = 151.2093;
        // Use a small precision for Sydney
        String hash = GeoHash.encodeHash(lat, lon, 7);
        LatLong decoded = GeoHash.decodeHash(hash);
        assertTrue(Math.abs(decoded.getLat() - lat) < 0.01, "Latitude close to input");
        assertTrue(Math.abs(decoded.getLon() - lon) < 0.01, "Longitude close to input");
    }

    @Test
    public void testEncodeDecodeWithZeroValues() {
        double lat = 0.0;
        double lon = 10.123456;
        String hash = GeoHash.encodeHash(lat, lon, 8);
        LatLong decoded = GeoHash.decodeHash(hash);
        assertTrue(Math.abs(decoded.getLat() - lat) < 0.01, "Latitude close to input");
        assertTrue(Math.abs(decoded.getLon() - lon) < 0.01, "Longitude close to input");
    }
}
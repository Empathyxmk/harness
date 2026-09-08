package com.github.davidmoten.geo;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class CoveragePublicTest {

    @Test
    public void testCoverageOfBoundingBoxWithDifferentData() {
        double lat1 = -10.0;
        double lon1 = 120.0;
        double lat2 = -9.5;
        double lon2 = 120.5;
        int hashLen = 4;
        Coverage coverage = GeoHash.coverBoundingBox(lat1, lon1, lat2, lon2, hashLen);
        assertNotNull(coverage);
        assertEquals(hashLen, coverage.getHashLength());
        assertFalse(coverage.getHashes().isEmpty());
    }

    @Test
    public void testCoverageOptimalLengthDifferent() {
        double lat1 = 35.0, lon1 = 135.0, lat2 = 35.1, lon2 = 135.1;
        Coverage coverage = GeoHash.coverBoundingBox(lat1, lon1, lat2, lon2);
        assertNotNull(coverage);
        assertTrue(coverage.getHashLength() > 0);
        assertFalse(coverage.getHashes().isEmpty());
    }

    @Test
    public void testCoverageMaxHashesNullDifferent() {
        double lat1 = -5.0, lon1 = 140.0, lat2 = -5.0, lon2 = 141.0;
        Coverage coverage = GeoHash.coverBoundingBoxMaxHashes(lat1, lon1, lat2, lon2, 0);
        assertNull(coverage);
    }
}
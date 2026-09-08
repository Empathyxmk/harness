package com.github.davidmoten.geo;

import static com.github.davidmoten.geo.GeoHash.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Set;
import com.google.common.collect.Sets;
import org.junit.jupiter.api.Test;

/**
 * Public unit tests for {@link GeoHash} with different data.
 */
public class GeoHashPublicTest {

    private static final double TOKYO_LON = 139.6917;
    private static final double TOKYO_LAT = 35.6895;
    private static final double LONDON_LON = -0.1278;
    private static final double LONDON_LAT = 51.5074;
    private static final double PRECISION = 0.000000001;

    @Test
    public void encodeHashToLongDifferentData() {
        assertEquals(0xc819000000000002L, GeoHash.encodeHashToLong(35.6895, 139.6917, 2));
    }

    @Test
    public void fromLongToStringInvalidDifferent() {
        assertThrows(IllegalArgumentException.class, () -> GeoHash.fromLongToString(0x1ee));
    }

    @Test
    public void fromLongToStringZeroDifferent() {
        assertThrows(IllegalArgumentException.class, () -> GeoHash.fromLongToString(0));
    }

    @Test
    public void testDifferentLandmarkHashEncode() {
        assertEquals("xn774c06kdt4", encodeHash(35.6895, 139.6917));
    }

    @Test
    public void testLandmarkHashEncodeUsingLatLongObject() {
        assertEquals("xn774c06kdt4", encodeHash(new LatLong(35.6895, 139.6917)));
    }

    @Test
    public void testLandmarkHashDecode() {
        LatLong point = decodeHash("xn774c06kdt4");
        assertEquals(point.getLat(), 35.6895, PRECISION);
        assertEquals(point.getLon(), 139.6917, PRECISION);
    }

    @Test
    public void testFromGeoHashDotOrgDifferentPoint() {
        assertEquals("gcpuvnjdgn85", encodeHash(51.5074, -0.1278));
    }

    @Test
    public void testHashOfNonDefaultLengthDifferent() {
        assertEquals("gcpuvn", encodeHash(51.5074, -0.1278, 6));
    }

    @Test
    public void testAdjacentTopDifferent() {
        assertEquals("xn774c06kdt7", adjacentHash("xn774c06kdt4", Direction.TOP));
    }

    @Test
    public void testAdjacentBottomDifferent() {
        assertEquals("xn774c06kdt1", adjacentHash("xn774c06kdt4", Direction.BOTTOM));
    }

    @Test
    public void testAdjacentLeftDifferent() {
        assertEquals("xn774c06kdt3", adjacentHash("xn774c06kdt4", Direction.LEFT));
    }

    @Test
    public void testAdjacentRightDifferent() {
        assertEquals("xn774c06kdt5", adjacentHash("xn774c06kdt4", Direction.RIGHT));
    }

    @Test
    public void testNeighbouringHashesDifferent() {
        String center = "gcpuvn";
        Set<String> neighbours = Sets.newHashSet("gcpuvm","gcpuvp","gcpuvj","gcpuvs","gcpuvh","gcpuvt","gcpuvk","gcpuvq");
        assertEquals(neighbours, Sets.newHashSet(neighbours(center)));
    }

    @Test
    public void testHashDecodeOnBlankStringDifferent() {
        LatLong point = decodeHash("");
        assertEquals(0, point.getLat(), PRECISION);
        assertEquals(0, point.getLon(), PRECISION);
    }

    @Test
    public void testCoverBoundingBoxWithHashLength4AroundLondonAndTokyo() {
        Set<String> hashes = coverBoundingBox(LONDON_LAT, LONDON_LON, TOKYO_LAT, TOKYO_LON, 4).getHashes();

        assertEquals("gcpu", encodeHash(LONDON_LAT, LONDON_LON, 4));
        assertEquals("xn76", encodeHash(TOKYO_LAT, TOKYO_LON, 4));
        assertTrue(hashes.contains("gcpu"));
        assertTrue(hashes.contains("xn76"));
    }

    @Test
    public void testCoverBoundingBoxWithHashLengthOneAroundLondonAndTokyo() {
        Coverage coverage = coverBoundingBox(LONDON_LAT, LONDON_LON, TOKYO_LAT, TOKYO_LON, 1);
        assertEquals(Sets.newHashSet("g", "x"), coverage.getHashes());
        assertEquals(1, coverage.getHashLength());
    }

    @Test
    public void testCoverBoundingBoxWithOptimalHashLengthAroundLondonAndTokyo() {
        Coverage coverage = coverBoundingBox(LONDON_LAT, LONDON_LON, TOKYO_LAT, TOKYO_LON);
        assertTrue(coverage.getHashes().size() >= 1);
        assertTrue(coverage.getHashLength() >= 1);
    }

    @Test
    public void testCoverBoundingBoxWithHashLength3AroundLondonAndTokyo() {
        Set<String> hashes = coverBoundingBox(LONDON_LAT, LONDON_LON, TOKYO_LAT, TOKYO_LON, 3).getHashes();
        assertTrue(hashes.contains("gcp"));
        assertTrue(hashes.contains("xn7"));
    }

    @Test
    public void testCoverBoundingBoxWithZeroLengthThrowsExceptionPublic() {
        assertThrows(IllegalArgumentException.class, () ->
                coverBoundingBox(LONDON_LAT, LONDON_LON, TOKYO_LAT, TOKYO_LON, 0)
        );
    }
}
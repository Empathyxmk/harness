package com.github.davidmoten.geo;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
import java.util.Set;

public class CoverageLongsPublicTest {

    @Test
    public void testCoverageLongsForDifferentRegion() {
        double lat1 = 52.5, lon1 = 13.4, lat2 = 52.6, lon2 = 13.5;
        Set<Long> hashes = CoverageLongs.coverBoundingBoxLongs(lat1, lon1, lat2, lon2, 5).getHashes();
        assertNotNull(hashes);
        assertFalse(hashes.isEmpty());
    }

    @Test
    public void testCoverageLongsMaxHashesDifferent() {
        double lat1 = 48.8566, lon1 = 2.3522, lat2 = 48.8567, lon2 = 2.3523;
        CoverageLongs result = CoverageLongs.coverBoundingBoxMaxHashes(lat1, lon1, lat2, lon2, 1);
        assertNotNull(result);
        assertTrue(result.getHashLength() > 0);
    }

    @Test
    public void testCoverageLongsNullIfTooManyHashesDifferent() {
        double lat1 = 50.0, lon1 = -0.01, lat2 = 50.0, lon2 = 0.01;
        CoverageLongs result = CoverageLongs.coverBoundingBoxMaxHashes(lat1, lon1, lat2, lon2, 0);
        assertNull(result);
    }
}
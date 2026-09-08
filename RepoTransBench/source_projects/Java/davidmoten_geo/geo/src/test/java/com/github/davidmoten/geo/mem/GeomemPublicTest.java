package com.github.davidmoten.geo.mem;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

import com.github.davidmoten.geo.LatLong;

import java.util.List;

public class GeomemPublicTest {

    @Test
    public void testAddAndQueryDifferentValues() {
        Geomem<LatLong> geo = Geomem.create();
        // Use coordinates and label different from original tests
        geo.add(50.12, 8.68, 700, new LatLong(50.12, 8.68));
        geo.add(48.85, 2.35, 900, new LatLong(48.85, 2.35));

        List<Info<LatLong>> list = geo.find(49, 8, 350000);
        // Should include at least the first item for this radius and point
        assertEquals(1, list.size());
        assertEquals(50.12, list.get(0).getValue().getLat(), 1e-5);
        assertEquals(8.68, list.get(0).getValue().getLon(), 1e-5);
    }

    @Test
    public void testEmptyQueryDifferentArea() {
        Geomem<String> geo = Geomem.create();
        geo.add(37.77, -122.41, 100, "San Francisco");
        List<Info<String>> list = geo.find(41.89, 12.49, 1000); // Query near Rome
        // No results expected as locations are far apart
        assertTrue(list.isEmpty());
    }
}
package com.github.davidmoten.geo.mem;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

import com.github.davidmoten.geo.LatLong;

import java.util.List;

public class GeomemPublicTest {

    @Test
    public void testAddAndDifferentQuery() {
        Geomem<LatLong> geo = Geomem.create();
        // Different coordinates and label than any in the default test set
        geo.add(35.0, 139.0, 200, new LatLong(35.0, 139.0)); // Tokyo
        geo.add(51.5, -0.1, 180, new LatLong(51.5, -0.1)); // London

        List<Info<LatLong>> list = geo.find(35.5, 139.7, 100000); // Query near Tokyo, 100 km radius
        assertEquals(1, list.size());
        assertEquals(35.0, list.get(0).getValue().getLat(), 1e-5);
        assertEquals(139.0, list.get(0).getValue().getLon(), 1e-5);
    }

    @Test
    public void testNothingNearbyKnownAreas() {
        Geomem<String> geo = Geomem.create();
        geo.add(40.7128, -74.0060, 120, "NewYork");
        List<Info<String>> list = geo.find(-33.8688, 151.2093, 100); // Query near Sydney
        assertTrue(list.isEmpty());
    }
}
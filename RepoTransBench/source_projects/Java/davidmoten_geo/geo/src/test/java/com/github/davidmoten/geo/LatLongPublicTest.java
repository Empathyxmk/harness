package com.github.davidmoten.geo;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

/**
 * Public unit tests for {@link LatLong} with different data.
 */
public class LatLongPublicTest {

    @Test
    public void testToStringDifferentValue() {
        assertEquals("LatLong [lat=-15.25, lon=35.75]",
                new LatLong(-15.25, 35.75).toString());
    }

    @Test
    public void testHashCodeAndEqualsWithDifferentValues() {
        float lat = -30.42f;
        float lon = 44.44f;
        LatLong a = new LatLong(lat, lon);
        LatLong b = new LatLong(lat, lon);

        assertEquals(a.hashCode(), b.hashCode());
        assertEquals(a, b);
    }

}
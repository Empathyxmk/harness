package org.geojson;

import org.junit.Test;
import java.util.*;

import static org.junit.Assert.*;

public class public_GeometryPublicTest {
    static class DummyGeometry extends Geometry<String> {
        DummyGeometry() { super(); }
        DummyGeometry(String... vals) {
            super();
            setCoordinates(Arrays.asList(vals));
        }
        @Override
        public <T> T accept(GeoJsonObjectVisitor<T> visitor) { return null; }
    }

    @Test
    public void testAddAndGetCoordinates_public() {
        DummyGeometry g = new DummyGeometry();
        g.add("X").add("Y");
        List<String> coords = g.getCoordinates();
        assertEquals(2, coords.size());
        assertEquals("X", coords.get(0));
        assertEquals("Y", coords.get(1));
    }

    @Test
    public void testSetCoordinates_public() {
        DummyGeometry g = new DummyGeometry();
        List<String> c = Arrays.asList("alpha", "beta");
        g.setCoordinates(c);
        assertEquals(c, g.getCoordinates());
    }

    @Test
    public void testConstructorWithElements_public() {
        DummyGeometry g = new DummyGeometry("one", "two", "three");
        assertArrayEquals(new String[]{"one", "two", "three"}, g.getCoordinates().toArray());
    }

    @Test
    public void testEqualsAndHashCode_public() {
        DummyGeometry g1 = new DummyGeometry("aab");
        DummyGeometry g2 = new DummyGeometry("aab");
        assertEquals(g1, g2);
        assertEquals(g1.hashCode(), g2.hashCode());
        assertNotEquals(g1, null);
        assertNotEquals(g1, new Object()); // Should not be equal to unrelated class
        DummyGeometry g3 = new DummyGeometry("bbc");
        assertNotEquals(g1, g3);
    }

    @Test
    public void testToString_public() {
        DummyGeometry g = new DummyGeometry("z1");
        assertTrue(g.toString().contains("coordinates"));
    }
}
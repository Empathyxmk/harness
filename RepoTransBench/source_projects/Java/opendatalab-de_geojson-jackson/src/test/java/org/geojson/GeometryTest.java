package org.geojson;

import org.junit.Test;
import java.util.*;

import static org.junit.Assert.*;

public class GeometryTest {
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
    public void testAddAndGetCoordinates() {
        DummyGeometry g = new DummyGeometry();
        g.add("A").add("B");
        List<String> coords = g.getCoordinates();
        assertEquals(2, coords.size());
        assertEquals("A", coords.get(0));
    }

    @Test
    public void testSetCoordinates() {
        DummyGeometry g = new DummyGeometry();
        List<String> c = Arrays.asList("x", "y");
        g.setCoordinates(c);
        assertEquals(c, g.getCoordinates());
    }

    @Test
    public void testConstructorWithElements() {
        DummyGeometry g = new DummyGeometry("p", "q");
        assertArrayEquals(new String[]{"p","q"}, g.getCoordinates().toArray());
    }

    @Test
    public void testEqualsAndHashCode() {
        DummyGeometry g1 = new DummyGeometry("a");
        DummyGeometry g2 = new DummyGeometry("a");
        assertEquals(g1, g2);
        assertEquals(g1.hashCode(), g2.hashCode());
        assertNotEquals(g1, null);
        assertNotEquals(g1, new Feature());
        DummyGeometry g3 = new DummyGeometry("b");
        assertNotEquals(g1, g3);
    }

    @Test
    public void testToString() {
        DummyGeometry g = new DummyGeometry("a");
        assertTrue(g.toString().contains("coordinates"));
    }
}
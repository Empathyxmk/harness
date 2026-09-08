package org.geojson;

import org.junit.Test;
import java.util.Arrays;

import static org.junit.Assert.*;

public class LineStringUnitTest {
    @Test
    public void testConstructorAndAdd() {
        LngLatAlt p1 = new LngLatAlt(1,2);
        LngLatAlt p2 = new LngLatAlt(2,3);
        LineString line = new LineString(p1);
        line.add(p2);
        assertEquals(2, line.getCoordinates().size());
        assertEquals(p1, line.getCoordinates().get(0));
        assertEquals(p2, line.getCoordinates().get(1));
    }

    @Test
    public void testAccept() {
        LineString line = new LineString();
        String result = line.accept(new GeoJsonObjectVisitor<String>() {
            @Override public String visit(LineString ls) { return "ok"; }
            @Override public String visit(FeatureCollection fc) { return null; }
            @Override public String visit(Feature f) { return null; }
            @Override public String visit(Point p) { return null; }
            @Override public String visit(MultiPoint mp) { return null; }
            @Override public String visit(MultiLineString mls) { return null; }
            @Override public String visit(Polygon p) { return null; }
            @Override public String visit(MultiPolygon mp) { return null; }
            @Override public String visit(GeometryCollection gc) { return null; }
        });
        assertEquals("ok", result);
    }

    @Test
    public void testEqualsAndHashCode() {
        LineString l1 = new LineString(new LngLatAlt(1,2));
        LineString l2 = new LineString(new LngLatAlt(1,2));
        assertEquals(l1, l2);
        assertEquals(l1.hashCode(), l2.hashCode());
        assertNotEquals(l1, null);
        assertNotEquals(l1, new Object());
        LineString l3 = new LineString(new LngLatAlt(2,2));
        assertNotEquals(l1, l3);
    }

    @Test
    public void testToString() {
        LineString l = new LineString();
        assertTrue(l.toString().contains("coordinates"));
    }
}
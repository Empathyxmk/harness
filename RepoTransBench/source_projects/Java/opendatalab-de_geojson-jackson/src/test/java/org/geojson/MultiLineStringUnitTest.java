package org.geojson;

import org.junit.Test;

import static org.junit.Assert.*;

import java.util.Arrays;

public class MultiLineStringUnitTest {

    @Test
    public void testConstructorAndAdd() {
        LngLatAlt p1 = new LngLatAlt(1, 2);
        LngLatAlt p2 = new LngLatAlt(3, 4);

        LineString l1 = new LineString(p1);
        LineString l2 = new LineString(p2);

        MultiLineString mls = new MultiLineString();
        mls.add(l1.getCoordinates());
        mls.add(l2.getCoordinates());

        assertEquals(2, mls.getCoordinates().size());
        assertEquals(l1.getCoordinates(), mls.getCoordinates().get(0));
        assertEquals(l2.getCoordinates(), mls.getCoordinates().get(1));
    }

    @Test
    public void testAccept() {
        MultiLineString mls = new MultiLineString();
        String result = mls.accept(new GeoJsonObjectVisitor<String>() {
            @Override public String visit(MultiLineString v) { return "yes"; }
            @Override public String visit(FeatureCollection fc) { return null; }
            @Override public String visit(Feature f) { return null; }
            @Override public String visit(Point p) { return null; }
            @Override public String visit(MultiPoint mp) { return null; }
            @Override public String visit(LineString ls) { return null; }
            @Override public String visit(Polygon p) { return null; }
            @Override public String visit(MultiPolygon mp) { return null; }
            @Override public String visit(GeometryCollection gc) { return null; }
        });
        assertEquals("yes", result);
    }
}
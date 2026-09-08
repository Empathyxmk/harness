package org.geojson;

import org.junit.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.Assert.*;

public class public_FeatureUnitPublicTest {

    @Test
    public void testSetAndGetProperties_public() {
        Feature feature = new Feature();
        feature.setProperty("public_key", 321);
        assertEquals(321, (int) feature.getProperty("public_key"));

        Map<String, Object> map = new HashMap<>();
        map.put("alpha", "first");
        map.put("beta", 5);
        feature.setProperties(map);
        assertEquals("first", feature.getProperties().get("alpha"));
        assertEquals(5, feature.getProperties().get("beta"));
    }

    @Test
    public void testSetAndGetGeometry_public() {
        Feature feature = new Feature();
        Point p = new Point(55.5, 66.6);
        feature.setGeometry(p);
        assertSame(p, feature.getGeometry());
    }

    @Test
    public void testSetAndGetId_public() {
        Feature feature = new Feature();
        feature.setId("public_test_id");
        assertEquals("public_test_id", feature.getId());
    }

    @Test
    public void testEqualsAndHashCode_public() {
        Feature f1 = new Feature();
        f1.setProperty("x", 999);
        f1.setId("42");
        Feature f2 = new Feature();
        f2.setProperty("x", 999);
        f2.setId("42");
        assertEquals(f1, f2);
        assertEquals(f1.hashCode(), f2.hashCode());
        assertNotEquals(f1, null);
        assertNotEquals(f1, new Object());
        Feature f3 = new Feature();
        assertNotEquals(f1, f3);
    }

    @Test
    public void testToString_public() {
        Feature f = new Feature();
        String str = f.toString();
        assertTrue(str.contains("Feature"));
    }

    @Test
    public void testAccept_public() {
        Feature feature = new Feature();
        String result = feature.accept(new GeoJsonObjectVisitor<String>() {
            @Override public String visit(Feature f) {
                return "feature_visited_public";
            }
            @Override public String visit(Point p) { return null; }
            @Override public String visit(MultiPoint mp) { return null; }
            @Override public String visit(LineString ls) { return null; }
            @Override public String visit(MultiLineString mls) { return null; }
            @Override public String visit(Polygon p) { return null; }
            @Override public String visit(MultiPolygon mp) { return null; }
            @Override public String visit(GeometryCollection gc) { return null; }
            @Override public String visit(FeatureCollection fc) { return null; }
        });
        assertEquals("feature_visited_public", result);
    }
}
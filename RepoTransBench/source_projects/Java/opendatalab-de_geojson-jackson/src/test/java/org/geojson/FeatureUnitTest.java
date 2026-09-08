package org.geojson;

import org.junit.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.Assert.*;

public class FeatureUnitTest {
    @Test
    public void testPropertiesSetGet() {
        Feature feature = new Feature();
        feature.setProperty("key", "val");
        assertEquals("val", feature.getProperty("key"));
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("a", 1);
        feature.setProperties(map);
        assertEquals(map, feature.getProperties());
    }

    @Test
    public void testGeometrySetGet() {
        Feature feature = new Feature();
        Point p = new Point();
        feature.setGeometry(p);
        assertEquals(p, feature.getGeometry());
    }

    @Test
    public void testIdSetGet() {
        Feature feature = new Feature();
        feature.setId("x");
        assertEquals("x", feature.getId());
    }

    @Test
    public void testAccept() {
        Feature feature = new Feature();
        String result = feature.accept(new GeoJsonObjectVisitor<String>() {
            @Override
            public String visit(Feature f) { return "visited"; }
            @Override
            public String visit(FeatureCollection fc) { return null; }
            @Override
            public String visit(Point p) { return null; }
            @Override
            public String visit(MultiPoint mp) { return null; }
            @Override
            public String visit(LineString ls) { return null; }
            @Override
            public String visit(MultiLineString mls) { return null; }
            @Override
            public String visit(Polygon p) { return null; }
            @Override
            public String visit(MultiPolygon mp) { return null; }
            @Override
            public String visit(GeometryCollection gc) { return null; }
        });
        assertEquals("visited", result);
    }

    @Test
    public void testEqualsAndHashCode() {
        Feature f1 = new Feature();
        Feature f2 = new Feature();
        f1.setId("1"); f2.setId("1");
        f1.setProperty("x", "y"); f2.setProperty("x", "y");
        f1.setGeometry(new Point()); f2.setGeometry(new Point());
        assertEquals(f1, f2);
        assertEquals(f1.hashCode(), f2.hashCode());
        assertNotEquals(f1, null);
        assertNotEquals(f1, new Object());
        f2.setId("2");
        assertNotEquals(f1, f2);
    }

    @Test
    public void testToString() {
        Feature feature = new Feature();
        assertTrue(feature.toString().contains("Feature{"));
    }
}
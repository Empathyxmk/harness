package org.geojson;

import org.junit.Test;

import java.util.Arrays;

import static org.junit.Assert.*;

public class public_FeatureCollectionPublicTest {

    @Test
    public void testAddAndGetFeatures_public() {
        FeatureCollection fc = new FeatureCollection();
        Feature feature1 = new Feature();
        feature1.setId("public_id1");
        Feature feature2 = new Feature();
        feature2.setId("public_id2");
        fc.add(feature1);
        fc.add(feature2);

        assertEquals(2, fc.getFeatures().size());
        assertTrue(fc.getFeatures().contains(feature1));
        assertTrue(fc.getFeatures().contains(feature2));
    }

    @Test
    public void testSetFeatures_public() {
        FeatureCollection fc = new FeatureCollection();
        Feature a = new Feature();
        Feature b = new Feature();
        fc.setFeatures(Arrays.asList(a, b));
        assertEquals(2, fc.getFeatures().size());
        assertSame(a, fc.getFeatures().get(0));
        assertSame(b, fc.getFeatures().get(1));
    }

    @Test
    public void testRemoveFeatures_public() {
        FeatureCollection fc = new FeatureCollection();
        Feature f1 = new Feature();
        f1.setId("one");
        Feature f2 = new Feature();
        f2.setId("two");
        fc.add(f1);
        fc.add(f2);
        assertEquals(2, fc.getFeatures().size());
        boolean removed = fc.getFeatures().remove(f1);
        assertTrue(removed);
        assertEquals(1, fc.getFeatures().size());
        // Additional check for robustness
        assertFalse(fc.getFeatures().contains(f1));
        assertTrue(fc.getFeatures().contains(f2));
    }

    @Test
    public void testAccept_public() {
        FeatureCollection fc = new FeatureCollection();
        String result = fc.accept(new GeoJsonObjectVisitor<String>() {
            @Override public String visit(FeatureCollection fc) { return "public_fc_visited"; }
            @Override public String visit(Point p) { return null; }
            @Override public String visit(MultiPoint mp) { return null; }
            @Override public String visit(LineString ls) { return null; }
            @Override public String visit(MultiLineString mls) { return null; }
            @Override public String visit(Polygon p) { return null; }
            @Override public String visit(MultiPolygon mp) { return null; }
            @Override public String visit(GeometryCollection gc) { return null; }
            @Override public String visit(Feature f) { return null; }
        });
        assertEquals("public_fc_visited", result);
    }

    @Test
    public void testToString_public() {
        FeatureCollection fc = new FeatureCollection();
        String str = fc.toString();
        assertTrue(str.contains("FeatureCollection"));
    }

    @Test
    public void testEqualsAndHashCode_public() {
        FeatureCollection fc1 = new FeatureCollection();
        FeatureCollection fc2 = new FeatureCollection();
        Feature f1 = new Feature();
        f1.setId("uniqX");
        Feature f2 = new Feature();
        f2.setId("uniqY");
        fc1.add(f1);
        fc1.add(f2);
        fc2.setFeatures(Arrays.asList(f1, f2));
        assertEquals(fc1, fc2);
        assertEquals(fc1.hashCode(), fc2.hashCode());
        assertNotEquals(fc1, null);
        assertNotEquals(fc1, new Object());
        FeatureCollection fc3 = new FeatureCollection();
        Feature f3 = new Feature();
        f3.setId("different_id_for_public");
        fc3.add(f3);
        assertNotEquals(fc1, fc3);
    }

    @Test
    public void testGetFeaturesNeverNull_public() {
        FeatureCollection fc = new FeatureCollection();
        assertNotNull(fc.getFeatures());
        assertEquals(0, fc.getFeatures().size());
    }
}
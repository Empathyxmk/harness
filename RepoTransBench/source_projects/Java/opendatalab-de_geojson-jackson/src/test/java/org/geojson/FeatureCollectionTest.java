package org.geojson;

import org.junit.Test;
import java.util.*;

import static org.junit.Assert.*;

public class FeatureCollectionTest {

    @Test
    public void testAddAndGetFeatures() {
        FeatureCollection fc = new FeatureCollection();
        Feature f1 = new Feature();
        Feature f2 = new Feature();
        fc.add(f1).add(f2);

        List<Feature> features = fc.getFeatures();
        assertEquals(2, features.size());
        assertTrue(features.contains(f1));
        assertTrue(features.contains(f2));
    }

    @Test
    public void testSetFeatures() {
        FeatureCollection fc = new FeatureCollection();
        Feature f = new Feature();
        List<Feature> lst = new ArrayList<Feature>();
        lst.add(f);
        fc.setFeatures(lst);
        assertEquals(lst, fc.getFeatures());
    }

    @Test
    public void testAddAll() {
        FeatureCollection fc = new FeatureCollection();
        Feature f1 = new Feature();
        Feature f2 = new Feature();
        List<Feature> lst = Arrays.asList(f1, f2);
        fc.addAll(lst);
        assertTrue(fc.getFeatures().containsAll(lst));
    }

    @Test
    public void testIterator() {
        FeatureCollection fc = new FeatureCollection();
        Feature f1 = new Feature();
        fc.add(f1);
        Iterator<Feature> iterator = fc.iterator();
        assertTrue(iterator.hasNext());
        assertEquals(f1, iterator.next());
    }

    @Test
    public void testAccept() {
        FeatureCollection fc = new FeatureCollection();
        String result = fc.accept(new GeoJsonObjectVisitor<String>() {
            @Override
            public String visit(FeatureCollection fc) {
                return "visited";
            }
            @Override
            public String visit(Feature f) { return null; }
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
        FeatureCollection fc1 = new FeatureCollection();
        FeatureCollection fc2 = new FeatureCollection();
        Feature f = new Feature();
        fc1.add(f);
        fc2.add(f);
        assertEquals(fc1, fc2);
        assertEquals(fc1.hashCode(), fc2.hashCode());
        assertNotEquals(fc1, null);
        assertNotEquals(fc1, new Feature());
        FeatureCollection fc3 = new FeatureCollection();
        assertNotEquals(fc1, fc3);
    }

    @Test
    public void testToString() {
        FeatureCollection fc = new FeatureCollection();
        assertTrue(fc.toString().contains("features"));
    }
}
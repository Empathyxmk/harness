package org.geojson;

import org.junit.Test;

import static org.junit.Assert.*;

public class public_ToStringPublicTest {

    @Test
    public void testToString_public_Point() {
        Point point = new Point(18.9, -77.5);
        String str = point.toString();
        assertTrue(str.contains("coordinates"));
        assertTrue(str.contains("18.9"));
    }

    @Test
    public void testToString_public_LineString() {
        LineString ls = new LineString(new LngLatAlt(88.1, 99.2));
        String str = ls.toString();
        assertTrue(str.contains("coordinates"));
        assertTrue(str.contains("88.1"));
    }

    @Test
    public void testToString_public_Feature() {
        Feature f = new Feature();
        f.setId("public_id");
        String str = f.toString();
        assertTrue(str.contains("id='public_id'"));
    }
}
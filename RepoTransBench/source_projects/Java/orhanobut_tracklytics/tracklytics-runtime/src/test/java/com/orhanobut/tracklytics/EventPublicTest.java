package com.orhanobut.tracklytics;

import org.junit.Test;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import static org.junit.Assert.*;

public class EventPublicTest {

    static class CustomTrackEvent implements TrackEvent {
        @Override public String value() { return "public_event"; }
        @Override public int[] filters() { return new int[]{3,4}; }
        @Override public String[] tags() { return new String[]{"pub1","pub2"}; }
        @Override public Class<? extends java.lang.annotation.Annotation> annotationType() {
            return TrackEvent.class;
        }
    }

    @Test
    public void testConstructorWithDifferentFields() {
        String name = "demo";
        int[] filters = new int[]{10,20};
        String[] tags = new String[]{"alpha","beta"};
        Map<String,Object> attrs = new HashMap<>();
        attrs.put("m", "n");
        Map<String,Object> superAttrs = new HashMap<>();
        superAttrs.put("foo", "bar");
        Event ev = new Event(name, filters, tags, attrs, superAttrs);
        assertEquals(name, ev.name);
        assertArrayEquals(filters, ev.filters);
        assertArrayEquals(tags, ev.tags);
        assertEquals(attrs, ev.attributes);
        assertEquals(superAttrs, ev.superAttributes);
    }

    @Test
    public void testConstructorWithDifferentTrackEvent() {
        TrackEvent te = new CustomTrackEvent();
        Map<String,Object> attrs = new HashMap<>();
        attrs.put("x", 2);
        Map<String,Object> superAttrs = Collections.singletonMap("y", "z");
        Event ev = new Event(te, attrs, superAttrs);
        assertEquals("public_event", ev.name);
        assertArrayEquals(new int[]{3,4}, ev.filters);
        assertArrayEquals(new String[]{"pub1","pub2"}, ev.tags);
        assertEquals(attrs, ev.attributes);
        assertEquals(superAttrs, ev.superAttributes);
    }

    @Test
    public void testGetAllAttributesDifferentKeys() {
        Map<String,Object> attrs = new HashMap<>();
        attrs.put("jack", "jill");
        Map<String,Object> superAttrs = new HashMap<>();
        superAttrs.put("tango", "fox");
        Event ev = new Event("n2", new int[0], new String[0], attrs, superAttrs);
        Map<String, Object> all = ev.getAllAttributes();
        assertEquals(2, all.size());
        assertEquals("jill", all.get("jack"));
        assertEquals("fox", all.get("tango"));
    }

    @Test
    public void testGetAllAttributesSuperOverridesDifferent() {
        Map<String,Object> attrs = new HashMap<>();
        attrs.put("theme", "dark");
        attrs.put("score", 100);
        Map<String,Object> superAttrs = new HashMap<>();
        superAttrs.put("theme", "light"); // same key as attrs, value different
        Event ev = new Event("n3", new int[0], new String[0], attrs, superAttrs);
        Map<String, Object> all = ev.getAllAttributes();
        assertEquals(2, all.size());
        assertEquals("light", all.get("theme")); // superAttribute overrides
        assertEquals(100, all.get("score"));
    }

    @Test
    public void testEmptyAttributesPublic() {
        Event event = new Event("public_event", new int[0], new String[0], Collections.emptyMap(), Collections.emptyMap());
        assertNotNull(event.getAllAttributes());
        assertTrue(event.getAllAttributes().isEmpty());
    }
}
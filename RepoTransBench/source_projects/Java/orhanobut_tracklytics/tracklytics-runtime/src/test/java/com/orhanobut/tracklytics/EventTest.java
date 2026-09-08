package com.orhanobut.tracklytics;

import org.junit.Test;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import static org.junit.Assert.*;

public class EventTest {

    static class DummyTrackEvent implements TrackEvent {
        @Override public String value() { return "dummy_event"; }
        @Override public int[] filters() { return new int[]{1,2}; }
        @Override public String[] tags() { return new String[]{"tag1","tag2"}; }
        @Override public Class<? extends java.lang.annotation.Annotation> annotationType() {
            return TrackEvent.class;
        }
    }

    @Test
    public void testConstructorWithFields() {
        String name = "test";
        int[] filters = new int[]{1,2};
        String[] tags = new String[]{"t1","t2"};
        Map<String,Object> attrs = new HashMap<>();
        attrs.put("a", "b");
        Map<String,Object> superAttrs = new HashMap<>();
        superAttrs.put("x", "y");
        Event ev = new Event(name, filters, tags, attrs, superAttrs);
        assertEquals(name, ev.name);
        assertArrayEquals(filters, ev.filters);
        assertArrayEquals(tags, ev.tags);
        assertEquals(attrs, ev.attributes);
        assertEquals(superAttrs, ev.superAttributes);
    }

    @Test
    public void testConstructorWithTrackEvent() {
        TrackEvent te = new DummyTrackEvent();
        Map<String,Object> attrs = new HashMap<>();
        attrs.put("c", 1);
        Map<String,Object> superAttrs = Collections.emptyMap();
        Event ev = new Event(te, attrs, superAttrs);
        assertEquals("dummy_event", ev.name);
        assertArrayEquals(new int[]{1,2}, ev.filters);
        assertArrayEquals(new String[]{"tag1","tag2"}, ev.tags);
        assertEquals(attrs, ev.attributes);
        assertEquals(superAttrs, ev.superAttributes);
    }

    @Test
    public void testGetAllAttributesNoOverlap() {
        Map<String,Object> attrs = new HashMap<>();
        attrs.put("foo", "bar");
        Map<String,Object> superAttrs = new HashMap<>();
        superAttrs.put("hello", "world");
        Event ev = new Event("n", new int[0], new String[0], attrs, superAttrs);
        Map<String, Object> all = ev.getAllAttributes();
        assertEquals(2, all.size());
        assertEquals("bar", all.get("foo"));
        assertEquals("world", all.get("hello"));
    }

    @Test
    public void testGetAllAttributesSuperOverridesNormal() {
        Map<String,Object> attrs = new HashMap<>();
        attrs.put("foo", "bar");
        attrs.put("a", 1);
        Map<String,Object> superAttrs = new HashMap<>();
        superAttrs.put("foo", "baz"); // same key as attrs
        Event ev = new Event("n", new int[0], new String[0], attrs, superAttrs);
        Map<String, Object> all = ev.getAllAttributes();
        assertEquals(2, all.size());
        assertEquals("baz", all.get("foo")); // superAttribute overrides
        assertEquals(1, all.get("a"));
    }

    @Test
    public void testEmptyAttributes() {
        Event event = new Event("event", new int[0], new String[0], Collections.emptyMap(), Collections.emptyMap());
        assertNotNull(event.getAllAttributes());
        assertTrue(event.getAllAttributes().isEmpty());
    }
}
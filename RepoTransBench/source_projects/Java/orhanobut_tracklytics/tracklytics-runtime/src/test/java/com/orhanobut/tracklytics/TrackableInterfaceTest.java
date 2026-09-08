package com.orhanobut.tracklytics;

import org.junit.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.Assert.*;

public class TrackableInterfaceTest {
    static class DummyTrackable implements Trackable {
        @Override public Map<String, Object> getTrackableAttributes() {
            Map<String,Object> result = new HashMap<>();
            result.put("key", "val");
            return result;
        }
    }

    @Test
    public void testTrackableMethod() {
        Trackable t = new DummyTrackable();
        Map<String, Object> attrs = t.getTrackableAttributes();
        assertEquals(1, attrs.size());
        assertEquals("val", attrs.get("key"));
    }
}
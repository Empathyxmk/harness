package com.orhanobut.tracklytics;

import org.junit.Before;
import org.junit.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.Assert.*;

public class TracklyticsPublicTest {

    private Tracklytics tracklytics;

    @Before
    public void setUp() {
        tracklytics = new Tracklytics();
    }

    @Test
    public void testAddAndRemoveSuperAttributePublic() {
        tracklytics.addSuperAttribute("pubA", 42);
        assertEquals(42, tracklytics.getSuperAttributes().get("pubA"));

        tracklytics.removeSuperAttribute("pubA");
        assertFalse(tracklytics.getSuperAttributes().containsKey("pubA"));
    }

    @Test
    public void testTrackEventWithSuperAttributesPublic() {
        tracklytics.addSuperAttribute("pubX", 99);
        Map<String, Object> attrs = new HashMap<>();
        attrs.put("pubY", "fooBar");
        Event event = new Event("pEvent", new int[]{8}, new String[]{"pT"}, attrs, tracklytics.getSuperAttributes());
        // Check event contains merged attributes
        Map<String, Object> all = event.getAllAttributes();
        assertEquals("fooBar", all.get("pubY"));
        assertEquals(99, all.get("pubX"));
    }
}
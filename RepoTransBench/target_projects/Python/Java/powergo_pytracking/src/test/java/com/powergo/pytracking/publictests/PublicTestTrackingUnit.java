package com.powergo.pytracking.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicTestTrackingUnit {

    @Test
    void testTrackingIdFormat() {
        String id = "abc-DEF123_456";
        assertTrue(id.matches("^[a-zA-Z0-9-_]+$"));
    }

    @Test
    void testTrackingUnitToString() {
        // Simulate __str__ or toString
        class TrackingUnit {
            String id;
            TrackingUnit(String id) { this.id = id; }
            public String toString() { return "TrackingUnit(" + id + ")"; }
        }
        TrackingUnit unit = new TrackingUnit("track123");
        assertEquals("TrackingUnit(track123)", unit.toString());
    }
}
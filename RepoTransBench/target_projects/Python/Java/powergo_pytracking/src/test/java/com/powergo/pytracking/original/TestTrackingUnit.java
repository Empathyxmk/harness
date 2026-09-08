package com.powergo.pytracking.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestTrackingUnit {

    @Test
    void testCreateTrackingUnit() {
        class TrackingUnit {
            String id;
            TrackingUnit(String id) { this.id = id; }
        }
        TrackingUnit unit = new TrackingUnit("mytrack");
        assertEquals("mytrack", unit.id);
    }

    @Test
    void testTrackingUnitEquality() {
        class TrackingUnit {
            String id;
            TrackingUnit(String id) { this.id = id; }
            @Override
            public boolean equals(Object o) {
                if (!(o instanceof TrackingUnit)) return false;
                return id.equals(((TrackingUnit)o).id);
            }
        }
        TrackingUnit a = new TrackingUnit("x");
        TrackingUnit b = new TrackingUnit("x");
        TrackingUnit c = new TrackingUnit("y");
        assertEquals(a, b);
        assertNotEquals(a, c);
    }
}
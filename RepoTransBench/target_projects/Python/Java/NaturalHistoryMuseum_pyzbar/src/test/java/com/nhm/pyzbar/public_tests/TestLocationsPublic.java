package com.nhm.pyzbar.public_tests;

import com.nhm.pyzbar.locations.BoundingBoxUtils;
import com.nhm.pyzbar.locations.Rect;
import org.junit.jupiter.api.Test;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class TestLocationsPublic {
    @Test
    void testPolygonFromBbox() {
        int x1 = 3, y1 = 4, x2 = 16, y2 = 22;
        List<Rect> polygon = BoundingBoxUtils.polygonFromBbox(x1, y1, x2, y2);
        assertEquals(Arrays.asList(
                new Rect(3, 4),
                new Rect(16, 4),
                new Rect(16, 22),
                new Rect(3, 22)
        ), polygon);
    }

    @Test
    void testPolygonFromBboxZeroWidthHeight() {
        int x1 = 10, y1 = 10, x2 = 10, y2 = 25;
        List<Rect> polygon = BoundingBoxUtils.polygonFromBbox(x1, y1, x2, y2);
        assertEquals(Arrays.asList(
                new Rect(10, 10),
                new Rect(10, 10),
                new Rect(10, 25),
                new Rect(10, 25)
        ), polygon);
    }
}
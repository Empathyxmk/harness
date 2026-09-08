package com.nhm.pyzbar.public_tests;

import com.nhm.pyzbar.locations.BoundingBoxUtils;
import com.nhm.pyzbar.locations.Rect;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class TestBoundingBoxAndPolygonPublic {

    @Test
    void testBoundingBoxRect() {
        // pts for bounding box
        List<Rect> pts = Arrays.asList(
                new Rect(5, 7), new Rect(25, 7), new Rect(25, 32), new Rect(5, 32)
        );
        Rect box = BoundingBoxUtils.boundingBoxRect(pts);
        assertEquals(new Rect(5, 7, 20, 25), box); // (minX, minY, width, height)
        // Mix order for robustness
        List<Rect> ptsReorder = Arrays.asList(
                new Rect(25, 32), new Rect(25, 7), new Rect(5, 32), new Rect(5, 7)
        );
        Rect box2 = BoundingBoxUtils.boundingBoxRect(ptsReorder);
        assertEquals(new Rect(5, 7, 20, 25), box2);
    }

    @Test
    void testBoundingBoxNegativeCoords() {
        List<Rect> pts = Arrays.asList(
                new Rect(-12, -8), new Rect(0, -8), new Rect(0, 2), new Rect(-12, 2)
        );
        Rect box = BoundingBoxUtils.boundingBoxRect(pts);
        assertEquals(new Rect(-12, -8, 12, 10), box);
    }
}
package com.nhm.pyzbar.original;

import com.nhm.pyzbar.locations.BoundingBoxUtils;
import com.nhm.pyzbar.locations.Rect;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class TestLocations {
    @Test
    void testBoundingBox() {
        // bounding_box throws for empty input
        assertThrows(IllegalArgumentException.class, () -> BoundingBoxUtils.boundingBox(Collections.emptyList()));
        // bounding_box of singleton yields 0,0,0,0
        assertEquals(new Rect(0, 0, 0, 0), BoundingBoxUtils.boundingBox(Arrays.asList(new int[]{0, 0})));

        assertEquals(
                new Rect(37, 550, 324, 76),
                BoundingBoxUtils.boundingBox(Arrays.asList(
                        new int[]{37, 551}, new int[]{37, 625}, new int[]{361, 626}, new int[]{361, 550}
                ))
        );
    }

    @Test
    void testConvexHullEmpty() {
        assertEquals(Collections.emptyList(), BoundingBoxUtils.convexHull(Collections.emptyList()));
    }

    @Test
    void testConvexSquare() {
        List<int[]> points = Arrays.asList(new int[]{0, 0}, new int[]{0, 1}, new int[]{1, 1}, new int[]{1, 0});
        assertEquals(points, BoundingBoxUtils.convexHull(points));
    }

    @Test
    void testConvexDuplicates() {
        List<int[]> points = Arrays.asList(new int[]{0, 0}, new int[]{0, 1}, new int[]{1, 1}, new int[]{1, 0});
        List<int[]> repeated = Arrays.asList(
                new int[]{0, 0}, new int[]{0, 1}, new int[]{1, 1}, new int[]{1, 0},
                new int[]{0, 0}, new int[]{0, 1}, new int[]{1, 1}, new int[]{1, 0}
        );
        assertEquals(points, BoundingBoxUtils.convexHull(repeated));
    }

    @Test
    void testOtherConvexHulls() {
        List<int[]> pts1 = Arrays.asList(
                new int[]{1, 1}, new int[]{2, 2}, new int[]{3, 3}, new int[]{1, 3}
        );
        List<int[]> expected1 = Arrays.asList(new int[]{1, 1}, new int[]{1, 3}, new int[]{3, 3});
        assertEquals(expected1, BoundingBoxUtils.convexHull(pts1));
        List<int[]> pts2 = Arrays.asList(
                new int[]{4, 14}, new int[]{6, 15}, new int[]{7, 13}, new int[]{2, 11}, new int[]{9, 14},
                new int[]{13, 11}, new int[]{10, 12}, new int[]{7, 9}, new int[]{3, 7}, new int[]{1, 5},
                new int[]{5, 2}, new int[]{8, 5}, new int[]{11, 10}, new int[]{14, 7}, new int[]{13, 3},
                new int[]{11, 1}
        );
        List<int[]> expected2 = Arrays.asList(
                new int[]{1, 5}, new int[]{2, 11}, new int[]{4, 14}, new int[]{6, 15}, new int[]{9, 14},
                new int[]{13, 11}, new int[]{14, 7}, new int[]{13, 3}, new int[]{11, 1}, new int[]{5, 2}
        );
        assertEquals(expected2, BoundingBoxUtils.convexHull(pts2));
    }
}
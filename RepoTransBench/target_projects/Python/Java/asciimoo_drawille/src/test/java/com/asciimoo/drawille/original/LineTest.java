package com.asciimoo.drawille.original;

import com.asciimoo.drawille.LineUtil;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class LineTest {

    @Test
    void testSinglePixel() {
        List<int[]> pts = LineUtil.line(0, 0, 0, 0);
        assertEquals(1, pts.size());
        assertArrayEquals(new int[]{0,0}, pts.get(0));
    }

    @Test
    void testRow() {
        List<int[]> pts = LineUtil.line(0, 0, 1, 0);
        assertEquals(2, pts.size());
        assertArrayEquals(new int[]{0,0}, pts.get(0));
        assertArrayEquals(new int[]{1,0}, pts.get(1));
    }

    @Test
    void testColumn() {
        List<int[]> pts = LineUtil.line(0, 0, 0, 1);
        assertEquals(2, pts.size());
        assertArrayEquals(new int[]{0,0}, pts.get(0));
        assertArrayEquals(new int[]{0,1}, pts.get(1));
    }

    @Test
    void testDiagonal() {
        List<int[]> pts = LineUtil.line(0, 0, 1, 1);
        assertEquals(2, pts.size());
        assertArrayEquals(new int[]{0,0}, pts.get(0));
        assertArrayEquals(new int[]{1,1}, pts.get(1));
    }
}
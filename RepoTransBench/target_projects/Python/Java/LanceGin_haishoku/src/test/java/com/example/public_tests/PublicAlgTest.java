package com.example.public_tests;

import com.example.haishoku.alg.Alg;
import org.junit.jupiter.api.Test;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class PublicAlgTest {

    @Test
    public void testRgb2hlsVariation() {
        int[] out = Alg.rgb2hls(new int[]{200, 150, 100});
        assertArrayEquals(new int[]{30, 150, 102}, out);
    }

    @Test
    public void testGetHistogramVariation() {
        List<int[]> colors = Arrays.asList(
                new int[]{100, 100, 100},
                new int[]{100, 100, 100},
                new int[]{50, 50, 50});
        Map<int[], Integer> hist = Alg.getHistogram(colors);
        assertEquals(2, (int) hist.get(new int[]{100, 100, 100}));
        assertEquals(1, (int) hist.get(new int[]{50, 50, 50}));
    }
}
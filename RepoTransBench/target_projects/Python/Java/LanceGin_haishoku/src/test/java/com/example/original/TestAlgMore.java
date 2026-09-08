package com.example.original;

import com.example.haishoku.alg.Alg;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class TestAlgMore {

    @Test
    public void testSortByRgbBasic() {
        List<Map.Entry<Integer, int[]>> colors = Arrays.asList(
                new AbstractMap.SimpleEntry<>(10, new int[]{52, 150, 70}),
                new AbstractMap.SimpleEntry<>(4, new int[]{200, 100, 30}),
                new AbstractMap.SimpleEntry<>(7, new int[]{100, 120, 140})
        );
        List<Map.Entry<Integer, int[]>> result = Alg.sortByRgb(colors);
        assertEquals(10, result.get(0).getKey());
        assertArrayEquals(new int[]{52, 150, 70}, result.get(0).getValue());
        assertEquals(7, result.get(1).getKey());
        assertArrayEquals(new int[]{100, 120, 140}, result.get(1).getValue());
        assertEquals(4, result.get(2).getKey());
        assertArrayEquals(new int[]{200, 100, 30}, result.get(2).getValue());
    }

    @Test
    public void testRgbMaximumBasic() {
        List<Map.Entry<Integer, int[]>> colors = Arrays.asList(
                new AbstractMap.SimpleEntry<>(2, new int[]{10, 20, 30}),
                new AbstractMap.SimpleEntry<>(5, new int[]{40, 50, 60}),
                new AbstractMap.SimpleEntry<>(3, new int[]{25, 35, 45})
        );
        Map<String, Double> result = Alg.rgbMaximum(colors);
        assertEquals(40, result.get("r_max"));
        assertEquals(10, result.get("r_min"));
        assertEquals(50, result.get("g_max"));
        assertEquals(20, result.get("g_min"));
        assertEquals(60, result.get("b_max"));
        assertEquals(30, result.get("b_min"));
        assertTrue(Math.abs(result.get("r_dvalue") - 10.0) < 1e-6);
        assertTrue(Math.abs(result.get("g_dvalue") - 10.0) < 1e-6);
        assertTrue(Math.abs(result.get("b_dvalue") - 10.0) < 1e-6);
    }

    @Test
    public void testGroupByAccuracyEdge() {
        List<Map.Entry<Integer, int[]>> colors = Arrays.asList(
                new AbstractMap.SimpleEntry<>(2, new int[]{10, 20, 30}),
                new AbstractMap.SimpleEntry<>(1, new int[]{11, 21, 31})
        );
        List<List<List<List<Map.Entry<Integer, int[]>>>>> grouped = Alg.groupByAccuracy(colors, 1);
        int found = 0;
        for (List<List<List<Map.Entry<Integer, int[]>>>> rgbl : grouped)
            for (List<List<Map.Entry<Integer, int[]>>> rgl : rgbl)
                for (List<Map.Entry<Integer, int[]>> cell : rgl)
                    found += cell.size();
        assertEquals(2, found);
    }

    @Test
    public void testGroupByAccuracyLargeRange() {
        List<Map.Entry<Integer, int[]>> colors = Arrays.asList(
                new AbstractMap.SimpleEntry<>(1, new int[]{0, 0, 0}),
                new AbstractMap.SimpleEntry<>(1, new int[]{127, 127, 127}),
                new AbstractMap.SimpleEntry<>(1, new int[]{255, 255, 255})
        );
        List<List<List<List<Map.Entry<Integer, int[]>>>>> grouped = Alg.groupByAccuracy(colors, 3);
        List<Map.Entry<Integer, int[]>> out = new ArrayList<>();
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 3; j++)
                for (int k = 0; k < 3; k++)
                    out.addAll(grouped.get(i).get(j).get(k));
        assertEquals(3, out.size());
    }

    @Test
    public void testGetWeightedMeanWeighted() {
        List<Map.Entry<Integer, int[]>> group = Arrays.asList(
                new AbstractMap.SimpleEntry<>(10, new int[]{100, 150, 200}),
                new AbstractMap.SimpleEntry<>(10, new int[]{110, 130, 170})
        );
        Map.Entry<Integer, int[]> weighted = Alg.getWeightedMean(group);
        assertEquals(20, weighted.getKey());
        assertArrayEquals(new int[]{105, 140, 185}, weighted.getValue());
    }

    @Test
    public void testGetWeightedMeanSingle() {
        List<Map.Entry<Integer, int[]>> group = Collections.singletonList(
                new AbstractMap.SimpleEntry<>(1, new int[]{1, 2, 3}));
        Map.Entry<Integer, int[]> weighted = Alg.getWeightedMean(group);
        assertEquals(1, weighted.getKey());
        assertArrayEquals(new int[]{1, 2, 3}, weighted.getValue());
    }

    @Test
    public void testGroupByAccuracyAllSameColor() {
        List<Map.Entry<Integer, int[]>> colors = Arrays.asList(
                new AbstractMap.SimpleEntry<>(2, new int[]{10, 20, 30}),
                new AbstractMap.SimpleEntry<>(2, new int[]{10, 20, 30})
        );
        List<List<List<List<Map.Entry<Integer, int[]>>>>> grouped = Alg.groupByAccuracy(colors, 3);
        int found = 0;
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 3; j++)
                for (int k = 0; k < 3; k++)
                    found += grouped.get(i).get(j).get(k).size();
        assertEquals(2, found);
    }
}
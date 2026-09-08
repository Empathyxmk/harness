package com.example.original;

import com.example.haishoku.alg.Alg;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class TestAlg {

    private List<Map.Entry<Integer, int[]>> colorsTuple;
    private List<Map.Entry<Integer, int[]>> sortedTuple;

    public TestAlg() {
        colorsTuple = Arrays.asList(
                new AbstractMap.SimpleEntry<>(10, new int[]{100, 150, 200}),
                new AbstractMap.SimpleEntry<>(5, new int[]{120, 130, 140}),
                new AbstractMap.SimpleEntry<>(8, new int[]{110, 170, 130}),
                new AbstractMap.SimpleEntry<>(15, new int[]{90, 80, 210}),
                new AbstractMap.SimpleEntry<>(3, new int[]{180, 50, 60}),
                new AbstractMap.SimpleEntry<>(2, new int[]{240, 10, 20})
        );
        sortedTuple = Alg.sortByRgb(colorsTuple);
    }

    @Test
    public void testSortByRgb() {
        List<Map.Entry<Integer, int[]>> result = Alg.sortByRgb(colorsTuple);
        // Java will sort based on the value array, simulate by comparator or equals.
        // For testing, assume sort is by [R,G,B] ascending
        colorsTuple.sort(Comparator.comparing(entry -> Arrays.toString(entry.getValue())));
        assertEquals(colorsTuple, result);
    }

    @Test
    public void testRgbMaximum() {
        Map<String, Double> result = Alg.rgbMaximum(colorsTuple);
        assertEquals(240, result.get("r_max"));
        assertEquals(90, result.get("r_min"));
        assertEquals(170, result.get("g_max"));
        assertEquals(10, result.get("g_min"));
        assertEquals(210, result.get("b_max"));
        assertEquals(20, result.get("b_min"));
        assertTrue(result instanceof Map);
    }

    @Test
    public void testGroupByAccuracy() {
        List<List<List<List<Map.Entry<Integer, int[]>>>>> rgb = Alg.groupByAccuracy(sortedTuple, 3);
        assertEquals(3, rgb.size());
        assertEquals(3, rgb.get(0).size());
        assertEquals(3, rgb.get(0).get(0).size());
    }

    @Test
    public void testGetWeightedMean() {
        List<Map.Entry<Integer, int[]>> group = Arrays.asList(
                new AbstractMap.SimpleEntry<>(10, new int[]{100, 150, 200}),
                new AbstractMap.SimpleEntry<>(5, new int[]{120, 130, 140})
        );
        Map.Entry<Integer, int[]> wMean = Alg.getWeightedMean(group);
        assertNotNull(wMean);
        assertTrue(wMean.getKey() instanceof Integer);
        assertTrue(wMean.getValue() instanceof int[]);
        assertEquals(2, wMean.getValue().length);
    }

    @Test
    public void testGetWeightedMeanSingle() {
        List<Map.Entry<Integer, int[]>> group = Collections.singletonList(
                new AbstractMap.SimpleEntry<>(7, new int[]{50, 60, 70})
        );
        Map.Entry<Integer, int[]> wMean = Alg.getWeightedMean(group);
        assertEquals(7, wMean.getKey());
        assertArrayEquals(new int[]{50, 60, 70}, wMean.getValue());
    }

    @Test
    public void testGetWeightedMeanZero() {
        assertThrows(ArithmeticException.class, () -> Alg.getWeightedMean(Collections.emptyList()));
    }
}
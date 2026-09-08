package com.example.public_tests;

import com.example.haishoku.alg.Alg;
import org.junit.jupiter.api.Test;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class PublicAlgMoreTest {

    @Test
    public void testSortColorVariation() {
        Map<int[], Integer> colorHist = new HashMap<>();
        colorHist.put(new int[]{20,20,20}, 1);
        colorHist.put(new int[]{200,200,200}, 3);
        colorHist.put(new int[]{100,100,100}, 2);
        List<Map.Entry<int[], Integer>> result = Alg.sortColor(colorHist);
        assertArrayEquals(new int[]{200,200,200}, result.get(0).getKey());
        assertArrayEquals(new int[]{100,100,100}, result.get(1).getKey());
        assertArrayEquals(new int[]{20,20,20}, result.get(2).getKey());
    }

    @Test
    public void testGetColorDistinctVivid() {
        int[][] base = {
                {13,23,33}, {14,23,32}, {110,150,195}, {111,150,195}, {110,151,194}
        };
        List<int[]> res = Alg.getColor(Arrays.asList(base), 2);
        assertEquals(2, res.size());
        boolean foundTuple = false;
        for (int[] arr : res) {
            if (arr instanceof int[] && arr.length == 3) {
                foundTuple = true;
                break;
            }
        }
        assertTrue(foundTuple);
    }
}
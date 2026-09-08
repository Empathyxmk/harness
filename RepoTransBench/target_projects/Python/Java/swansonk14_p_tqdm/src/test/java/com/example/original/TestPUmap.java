package com.example.original;

import org.junit.jupiter.api.*;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;

public class TestPUmap {
    private int add1(int a) { return a + 1; }
    private int add2(int a, int b) { return a + b; }
    private int add3(int a, int b, int c) { return a + 2*b + 3*c; }

    @Test
    void testOneList() {
        List<Integer> array = Arrays.asList(1,2,3);
        Set<Integer> result = PseudoParallel.pUmap(this::add1, array);
        Set<Integer> correct = new HashSet<>(Arrays.asList(2,3,4));
        assertEquals(correct, result);
    }
    @Test
    void testTwoLists() {
        List<Integer> a1 = Arrays.asList(1,2,3);
        List<Integer> a2 = Arrays.asList(10,11,12);
        Set<Integer> result = new HashSet<>(PseudoParallel.pMap(this::add2, a1, a2));
        Set<Integer> correct = new HashSet<>(Arrays.asList(11,13,15));
        assertEquals(correct, result);
    }
    @Test
    void testTwoListsAndOneSingle() {
        List<Integer> array1 = Arrays.asList(1,2,3);
        List<Integer> array2 = Arrays.asList(10,11,12);
        int single = 5;
        Set<Integer> result = new HashSet<>(PseudoParallel.pMap((b,c) -> add3(single, b, c), array1, array2));
        Set<Integer> correct = new HashSet<>(Arrays.asList(37,42,47));
        assertEquals(correct, result);
    }
}
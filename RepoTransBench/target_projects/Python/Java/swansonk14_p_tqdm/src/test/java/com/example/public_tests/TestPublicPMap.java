package com.example.public_tests;

import org.junit.jupiter.api.*;
import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;
import static org.junit.jupiter.api.Assertions.*;

class PublicParallel {
    public static <T,R> List<R> pMap(Function<T,R> f, List<T> arr) {
        List<R> out = new ArrayList<>();
        for (T x : arr) out.add(f.apply(x));
        return out;
    }
    public static <A,B,R> List<R> pMap(BiFunctionWithException<A,B,R> f, List<A> arr1, List<B> arr2) {
        List<R> out = new ArrayList<>();
        int n = Math.min(arr1.size(), arr2.size());
        for (int i = 0; i < n; ++i) out.add(f.apply(arr1.get(i), arr2.get(i)));
        return out;
    }
    public static <A,B,C,R> List<R> pMap(TriFunctionWithException<A,B,C,R> f, List<A> arr1, List<B> arr2, List<C> arr3) {
        List<R> out = new ArrayList<>();
        int n = Math.min(Math.min(arr1.size(), arr2.size()), arr3.size());
        for (int i = 0; i < n; ++i) out.add(f.apply(arr1.get(i), arr2.get(i), arr3.get(i)));
        return out;
    }
    public interface BiFunctionWithException<A,B,R> { R apply(A a, B b); }
    public interface TriFunctionWithException<A,B,C,R> { R apply(A a,B b,C c); }
}

public class TestPublicPMap {
    private int combineValues(int a, int b, int c) { return a + b*3 + c*4; }

    @Test
    void testTwoListsAndOneSingle() {
        List<Integer> array1 = Arrays.asList(2,8,14);
        List<Integer> array2 = Arrays.asList(7,1,4);
        int single = 5;
        List<Integer> result = PublicParallel.pMap((a,b) -> combineValues(a,b,single), array2, array1);
        List<Integer> correct = new ArrayList<>();
        for (int i = 0; i < 3; i++) correct.add(array2.get(i) + array1.get(i)*3 + single*4);
        assertEquals(correct, result);
    }
    @Test
    void testOneListAndTwoSingles() {
        List<Integer> array = Arrays.asList(20,25,28);
        int single1 = 4, single2 = 6;
        List<Integer> result = PublicParallel.pMap((a) -> combineValues(a, single1, single2), array);
        List<Integer> correct = new ArrayList<>();
        for (Integer v : array) correct.add(v + single1*3 + single2*4);
        assertEquals(correct, result);
    }
    @Test
    void testSingleList() {
        List<Integer> array = Arrays.asList(5,15,35);
        List<Integer> result = PublicParallel.pMap((a) -> combineValues(a,2,1), array);
        List<Integer> correct = new ArrayList<>();
        for (Integer v: array) correct.add(v + 2*3 + 1*4);
        assertEquals(correct, result);
    }
    @Test
    void testMultipleLists() {
        List<Integer> array1 = Arrays.asList(5,9,13);
        List<Integer> array2 = Arrays.asList(2,4,6);
        List<Integer> array3 = Arrays.asList(3,5,7);
        List<Integer> result = PublicParallel.pMap((a,b,c) -> combineValues(a,b,c), array1, array2, array3);
        List<Integer> correct = new ArrayList<>();
        for (int i = 0; i < 3; i++) correct.add(array1.get(i) + array2.get(i)*3 + array3.get(i)*4);
        assertEquals(correct, result);
    }
    @Test
    void testDifferentFunc() {
        List<Integer> list1 = Arrays.asList(1,3,5);
        List<Integer> list2 = Arrays.asList(2,4,6);
        List<Integer> result = PublicParallel.pMap((a,b) -> (int)Math.pow(a + b,3), list1, list2);
        assertEquals(Arrays.asList(27,343,1331), result);
    }
}
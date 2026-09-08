package com.example.original;

import org.junit.jupiter.api.*;
import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import static org.junit.jupiter.api.Assertions.*;

class PseudoParallel {
    // Util methods simulating the p_map and variants for tests
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
    // Ternary, simulate functools.partial of add_3
    public static <A,B,C,R> List<R> pMap(TriFunctionWithException<A,B,C,R> f, List<A> arr1, List<B> arr2, List<C> arr3) {
        List<R> out = new ArrayList<>();
        int n = Math.min(Math.min(arr1.size(), arr2.size()), arr3.size());
        for (int i = 0; i < n; ++i) out.add(f.apply(arr1.get(i), arr2.get(i), arr3.get(i)));
        return out;
    }

    // Generator sim: Return Iterable
    public static <T,R> Iterable<R> pImap(Function<T,R> f, List<T> arr) {
        return () -> arr.stream().map(f).iterator();
    }
    public static <A,B,R> Iterable<R> pImap(BiFunctionWithException<A,B,R> f, List<A> arr1, List<B> arr2) {
        List<R> out = pMap(f, arr1, arr2);
        return out;
    }


    // Unordered: use Set
    public static <T,R> Set<R> pUmap(Function<T,R> f, List<T> arr) {
        return arr.stream().map(f).collect(Collectors.toSet());
    }
    // Not strictly correct for unordered but for test suffices

    public interface BiFunctionWithException<A,B,R> { R apply(A a, B b); }
    public interface TriFunctionWithException<A,B,C,R> { R apply(A a,B b,C c); }
}

public class TestPMap {
    private int add1(int a) { return a + 1; }
    private int add2(int a, int b) { return a + b; }
    private int add3(int a, int b, int c) { return a + 2*b + 3*c; }

    // Like functools.partial(add3, a=..., c=...)
    private Function<Integer, Integer> partialAdd3WithAandC(int a, int c) {
        return (b) -> add3(a, b, c);
    }
    private PseudoParallel.BiFunctionWithException<Integer,Integer,Integer> partialAdd3WithA(int a) {
        return (b,c) -> add3(a,b,c);
    }
    private PseudoParallel.BiFunctionWithException<Integer,Integer,Integer> partialAdd3WithC(int c) {
        return (a,b) -> add3(a,b,c);
    }

    @Test
    void testOneList() {
        List<Integer> array = Arrays.asList(1,2,3);
        List<Integer> result = PseudoParallel.pMap(this::add1, array);
        List<Integer> correctArray = Arrays.asList(2,3,4);
        assertEquals(correctArray, result);
    }
    @Test
    void testTwoLists() {
        List<Integer> array1 = Arrays.asList(1,2,3);
        List<Integer> array2 = Arrays.asList(10,11,12);
        List<Integer> result = PseudoParallel.pMap(this::add2, array1, array2);
        List<Integer> correctArray = Arrays.asList(11,13,15);
        assertEquals(correctArray, result);
    }
    @Test
    void testTwoListsAndOneSingle() {
        List<Integer> array1 = Arrays.asList(1,2,3);
        List<Integer> array2 = Arrays.asList(10,11,12);
        int single = 5;
        List<Integer> result = PseudoParallel.pMap((b,c) -> add3(single, b, c), array1, array2);
        List<Integer> correctArray = Arrays.asList(37,42,47);
        assertEquals(correctArray, result);
    }

    @Test
    void testOneListAndTwoSingles() {
        List<Integer> array = Arrays.asList(1,2,3);
        int single1 = 5, single2 = -2;
        List<Integer> result = PseudoParallel.pMap(b -> add3(single1,b,single2), array);
        List<Integer> correctArray = Arrays.asList(1,3,5);
        assertEquals(correctArray, result);
    }

    @Test
    void testListAndGeneratorAndSingleEqualLength() {
        List<Integer> array = Arrays.asList(1,2,3);
        List<Integer> generator = Arrays.asList(0,1,2);
        int single = -3;
        List<Integer> result = PseudoParallel.pMap((a,b) -> add3(a,b,single), array, generator);
        List<Integer> correctArray = Arrays.asList(-8,-5,-2);
        assertEquals(correctArray, result);
    }
    @Test
    void testListAndGeneratorAndSingleUnequalLength() {
        List<Integer> array = Arrays.asList(1,2,3,4,5,6);
        List<Integer> generator = Arrays.asList(0,1,2);
        int single = -3;
        List<Integer> result = PseudoParallel.pMap((a,b) -> add3(a,b,single), array, generator);
        List<Integer> correctArray = Arrays.asList(-8,-5,-2);
        assertEquals(correctArray, result);
    }
}
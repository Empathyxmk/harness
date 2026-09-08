package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class PublicSequential {
    public static <T,R> List<R> sequential(Function<T,R> f, List<T> arr) {
        List<R> out = new ArrayList<>();
        for (T x : arr) out.add(f.apply(x));
        return out;
    }
    public static <A,B,R> List<R> sequential(BiFunction<A,B,R> f, List<A> arr1, List<B> arr2) {
        List<R> out = new ArrayList<>();
        int n = Math.min(arr1.size(), arr2.size());
        for (int i = 0; i < n; i++) out.add(f.apply(arr1.get(i), arr2.get(i)));
        return out;
    }
    public interface BiFunction<A,B,R> { R apply(A a, B b); }
}

public class TestPublicSequentialInternal {

    @Test
    void testSequential() {
        List<Integer> inList = Arrays.asList(2,4,6);
        List<Integer> out = PublicSequential.sequential(x -> x*3, inList);
        assertEquals(Arrays.asList(6,12,18), out);
    }
    @Test
    void testSequentialMultiple() {
        List<Integer> in1 = Arrays.asList(3,4);
        List<Integer> in2 = Arrays.asList(5,6);
        List<Integer> out = PublicSequential.sequential((a,b) -> a*b, in1, in2);
        assertEquals(Arrays.asList(15,24), out);
    }
    @Test
    void testSequentialLength() {
        List<Integer> in1 = Arrays.asList(2,3);
        List<Integer> in2 = Arrays.asList(7,11);
        List<Integer> out = PublicSequential.sequential((x,y) -> x*y*2, in1, in2);
        assertEquals(Arrays.asList(28,66), out);
    }
    @Test
    void testSequentialWithEmpty() {
        List<Integer> in = new ArrayList<>();
        List<Integer> out = PublicSequential.sequential(x -> x*10, in);
        assertEquals(Collections.emptyList(), out);
    }
    @Test
    void testSequentialWithException() {
        List<Integer> in = Arrays.asList(3,5,7);
        assertThrows(RuntimeException.class, () -> {
            PublicSequential.sequential(x -> {
                if (x == 5) throw new RuntimeException("terrible");
                return x*2;
            }, in);
        });
    }
}
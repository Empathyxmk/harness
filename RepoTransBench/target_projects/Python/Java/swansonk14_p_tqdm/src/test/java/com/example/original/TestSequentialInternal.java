package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class Sequential {
    public static <T,R> List<R> sequential(Function<T,R> f, List<T> arr) {
        List<R> out = new ArrayList<>();
        for (T x : arr) out.add(f.apply(x));
        return out;
    }
    public static <A,B,R> List<R> sequential(SeqBiFunction<A,B,R> f, List<A> arr1, List<B> arr2) {
        List<R> out = new ArrayList<>();
        int n = Math.min(arr1.size(), arr2.size());
        for (int i = 0; i < n; i++) {
            out.add(f.apply(arr1.get(i), arr2.get(i)));
        }
        return out;
    }
    public interface SeqBiFunction<A,B,R> { R apply(A a, B b); }
}

public class TestSequentialInternal {

    @Test
    void testSequential() {
        List<Integer> arr = Arrays.asList(1,2,3);
        List<Integer> out = Sequential.sequential(x -> x + 1, arr);
        assertEquals(Arrays.asList(2,3,4), out);
    }
    @Test
    void testSequentialMultiple() {
        List<Integer> arr1 = Arrays.asList(1,2);
        List<Integer> arr2 = Arrays.asList(2,3);
        List<Integer> out = Sequential.sequential((a,b) -> a + b, arr1, arr2);
        assertEquals(Arrays.asList(3,5), out);
    }
    @Test
    void testSequentialLength() {
        List<Integer> arr1 = Arrays.asList(1,2);
        List<Integer> arr2 = Arrays.asList(5,10);
        List<Integer> out = Sequential.sequential((a,b) -> a + b, arr1, arr2);
        assertEquals(Arrays.asList(6,12), out);
    }
    @Test
    void testSequentialWithEmpty() {
        List<Integer> inArr = new ArrayList<>();
        List<Integer> out = Sequential.sequential(x -> x, inArr);
        assertEquals(Collections.emptyList(), out);
    }
    @Test
    void testSequentialWithException() {
        List<Integer> arr = Arrays.asList(1,2,3);
        assertThrows(RuntimeException.class, () -> {
            Sequential.sequential(x -> {
                if (x == 2) throw new RuntimeException("bad");
                return x+1;
            }, arr);
        });
    }
}
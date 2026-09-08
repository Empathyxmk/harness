package com.viralogic.enumerable.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import java.util.stream.*;

class PyLinqTest {

    @Test
    void testPyLinqStyleSelectWhere() {
        List<Integer> numbers = Arrays.asList(1,2,3,4,5,6);
        List<Integer> evenSquares = numbers.stream()
            .filter(x -> x % 2 == 0)
            .map(x -> x * x)
            .collect(Collectors.toList());
        assertEquals(Arrays.asList(4, 16, 36), evenSquares);
    }

    @Test
    void testFirstOrDefault() {
        List<String> items = Arrays.asList("x", "y");
        String found = items.stream().filter(s -> s.equals("y")).findFirst().orElse("default");
        String notFound = items.stream().filter(s -> s.equals("z")).findFirst().orElse("default");
        assertEquals("y", found);
        assertEquals("default", notFound);
    }

    @Test
    void testSingleOrDefault() {
        List<String> items = Arrays.asList("only");
        String single = items.size() == 1 ? items.get(0) : "default";
        assertEquals("only", single);
        List<String> empty = Collections.emptyList();
        String emptyResult = empty.size() == 1 ? empty.get(0) : "default";
        assertEquals("default", emptyResult);
    }
}
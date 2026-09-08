package com.javaaid.search;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;
import java.util.Scanner;

class TripleSumTest {

    @Test
    void testTypicalCase() {
        int[] a = {1, 3, 5};
        int[] b = {2, 3};
        int[] c = {1, 2, 3};
        long expected = 8; // As per problem sample test
        assertEquals(expected, TripleSum.triplets(a, b, c));
    }

    @Test
    void testDuplicateValues() {
        int[] a = {1, 3, 5, 3};
        int[] b = {2, 3, 3};
        int[] c = {1, 2, 3, 1};
        long expected = 8; // Duplicates should not change outcome
        assertEquals(expected, TripleSum.triplets(a, b, c));
    }

    @Test
    void testAllZeros() {
        int[] a = {0, 0, 0};
        int[] b = {0, 0};
        int[] c = {0, 0};
        long expected = 1;
        assertEquals(expected, TripleSum.triplets(a, b, c));
    }

    @Test
    void testEmptyArrays() {
        int[] a = {};
        int[] b = {};
        int[] c = {};
        long expected = 0;
        assertEquals(expected, TripleSum.triplets(a, b, c));
    }

    @Test
    void testRemoveDuplicates() throws Exception {
        int[] arr = {1, 1, 2, 2, 3, 3, 3};
        java.lang.reflect.Method m = TripleSum.class.getDeclaredMethod("removeDuplicates", int[].class);
        m.setAccessible(true);
        int[] res = (int[]) m.invoke(null, arr);
        assertEquals(3, res.length);
        assertTrue(java.util.Arrays.stream(res).allMatch(x -> x == 1 || x == 2 || x == 3));
    }

    @Test
    void testGetValidIndex() throws Exception {
        java.lang.reflect.Method m = TripleSum.class.getDeclaredMethod("getValidIndex", int[].class, int.class);
        m.setAccessible(true);
        int[] arr = {1, 2, 3, 4, 5};
        assertEquals(2, (int) m.invoke(null, arr, 3)); // Should find last index <= 3 (which is 2)
        assertEquals(4, (int) m.invoke(null, arr, 6)); // Should return 4 (last index)
        assertEquals(-1, (int) m.invoke(null, arr, 0)); // Nothing <= 0
        assertEquals(0, (int) m.invoke(null, new int[]{2}, 2));
    }

    @Test
    void testMainExampleInput() {
        String input = "3 2 3\n1 3 5\n2 3\n1 2 3\n";
        InputStream oldIn = System.in;
        PrintStream oldOut = System.out;
        ByteArrayInputStream in = new ByteArrayInputStream(input.getBytes());
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        System.setIn(in);
        System.setOut(new PrintStream(out));

        TripleSum.main(new String[0]);
        System.setIn(oldIn);
        System.setOut(oldOut);
        String output = out.toString().trim();
        assertTrue(output.contains("8"));
    }

    @Test
    void testMainWithEmptyArrays() {
        String input = "0 0 0\n\n\n\n";
        InputStream oldIn = System.in;
        PrintStream oldOut = System.out;
        ByteArrayInputStream in = new ByteArrayInputStream(input.getBytes());
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        System.setIn(in);
        System.setOut(new PrintStream(out));

        TripleSum.main(new String[0]);
        System.setIn(oldIn);
        System.setOut(oldOut);
        String output = out.toString().trim();
        assertTrue(output.contains("0"));
    }
}
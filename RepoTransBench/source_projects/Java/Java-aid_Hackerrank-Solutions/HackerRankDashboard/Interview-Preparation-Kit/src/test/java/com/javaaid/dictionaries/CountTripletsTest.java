package com.javaaid.dictionaries;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import java.io.*;

class CountTripletsTest {

    @Test
    void testTypicalCase() {
        List<Long> arr = Arrays.asList(1L, 2L, 2L, 4L);
        long r = 2;
        long expected = 2;
        assertEquals(expected, invoke(arr, r));
    }

    @Test
    void testAllOnesR1() {
        List<Long> arr = Arrays.asList(1L, 1L, 1L, 1L);
        long r = 1;
        assertEquals(4, invoke(arr, r));
    }

    @Test
    void testNoTriplets() {
        List<Long> arr = Arrays.asList(1L, 2L, 4L, 8L);
        long r = 3;
        assertEquals(0, invoke(arr, r));
    }

    @Test
    void testSingleElement() {
        List<Long> arr = Arrays.asList(7L);
        long r = 2;
        assertEquals(0, invoke(arr, r));
    }

    @Test
    void testEmptyList() {
        List<Long> arr = new ArrayList<>();
        assertEquals(0, invoke(arr, 2L));
    }

    @Test
    void testMainTypicalCase() {
        String input = "4 2\n1 2 2 4\n";
        InputStream oldIn = System.in;
        PrintStream oldOut = System.out;
        ByteArrayInputStream in = new ByteArrayInputStream(input.getBytes());
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        System.setIn(in);
        System.setOut(new PrintStream(out));
        try {
            CountTriplets.main(new String[0]);
        } catch (Exception e) {
            fail("Should not throw: " + e);
        } finally {
            System.setIn(oldIn);
            System.setOut(oldOut);
        }
        String output = out.toString().trim();
        assertTrue(output.endsWith("2"));
    }

    @Test
    void testMainEmpty() {
        String input = "0 2\n";
        InputStream oldIn = System.in;
        PrintStream oldOut = System.out;
        ByteArrayInputStream in = new ByteArrayInputStream(input.getBytes());
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        System.setIn(in);
        System.setOut(new PrintStream(out));
        try {
            CountTriplets.main(new String[0]);
        } catch (Exception e) {
            fail("Should not throw: " + e);
        } finally {
            System.setIn(oldIn);
            System.setOut(oldOut);
        }
        String output = out.toString().replace("\n", "").trim();
        assertTrue(output.endsWith("0"));
    }

    private long invoke(List<Long> arr, long r) {
        // Use reflection since countTriplets is private
        try {
            java.lang.reflect.Method m = CountTriplets.class.getDeclaredMethod("countTriplets", List.class, long.class);
            m.setAccessible(true);
            return (long) m.invoke(null, arr, r);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
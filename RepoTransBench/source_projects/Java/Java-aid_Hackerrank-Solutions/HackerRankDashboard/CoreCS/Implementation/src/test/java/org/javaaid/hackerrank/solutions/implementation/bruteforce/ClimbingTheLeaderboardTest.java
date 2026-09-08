package org.javaaid.hackerrank.solutions.implementation.bruteforce;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;

class ClimbingTheLeaderboardTest {

    @Test
    void testTypicalCase() {
        int[] scores = {100, 100, 50, 40, 40, 20, 10};
        int[] alice = {5, 25, 50, 120};
        int[] expected = {6, 4, 2, 1};
        assertArrayEquals(expected, ClimbingTheLeaderboard.climbingLeaderboard(scores, alice));
    }

    @Test
    void testAllScoresSame() {
        int[] scores = {100, 100, 100};
        int[] alice = {50, 100, 101};
        int[] expected = {2, 1, 1};
        assertArrayEquals(expected, ClimbingTheLeaderboard.climbingLeaderboard(scores, alice));
    }

    @Test
    void testAliceAllLower() {
        int[] scores = {60, 30, 10};
        int[] alice = {5, 3};
        int[] expected = {4, 4};
        assertArrayEquals(expected, ClimbingTheLeaderboard.climbingLeaderboard(scores, alice));
    }

    @Test
    void testAliceAllHigher() {
        int[] scores = {40, 20, 10};
        int[] alice = {50};
        int[] expected = {1};
        assertArrayEquals(expected, ClimbingTheLeaderboard.climbingLeaderboard(scores, alice));
    }

    @Test
    void testSingleElementScores() {
        int[] scores = {100};
        int[] alice = {100, 101, 99};
        int[] expected = {1, 1, 2};
        assertArrayEquals(expected, ClimbingTheLeaderboard.climbingLeaderboard(scores, alice));
    }

    @Test
    void testBinarySearch() throws Exception {
        int[] a = {100, 90, 80, 70, 70, 60};
        java.lang.reflect.Method m = ClimbingTheLeaderboard.class.getDeclaredMethod("binarySearch", int[].class, int.class);
        m.setAccessible(true);
        assertEquals(3, m.invoke(null, a, 70));
        assertEquals(2, m.invoke(null, a, 85));
        assertEquals(1, m.invoke(null, a, 95));
        assertEquals(-1, m.invoke(null, a, 50));
    }

    @Test
    void testMainTypicalCase() {
        String input = "7\n100 100 50 40 40 20 10\n4\n5 25 50 120\n";
        InputStream oldIn = System.in;
        PrintStream oldOut = System.out;
        ByteArrayInputStream in = new ByteArrayInputStream(input.getBytes());
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        System.setIn(in);
        System.setOut(new PrintStream(out));
        ClimbingTheLeaderboard.main(new String[0]);
        System.setIn(oldIn);
        System.setOut(oldOut);
        String outStr = out.toString();
        assertTrue(outStr.contains("1") && outStr.contains("6"));
    }
}
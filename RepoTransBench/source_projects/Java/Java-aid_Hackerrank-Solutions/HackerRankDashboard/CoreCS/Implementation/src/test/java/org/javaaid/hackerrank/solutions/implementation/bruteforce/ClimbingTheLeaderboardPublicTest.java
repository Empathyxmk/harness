package org.javaaid.hackerrank.solutions.implementation.bruteforce;

import static org.junit.Assert.assertArrayEquals;

import java.util.Arrays;
import java.util.List;

import org.junit.Test;

public class ClimbingTheLeaderboardPublicTest {

    @Test
    public void testCustomCase1() {
        List<Integer> ranked = Arrays.asList(120, 100, 100, 50, 40, 40, 20, 10);
        List<Integer> player = Arrays.asList(5, 25, 45, 60, 105, 130);

        int[] expected = {8, 6, 4, 4, 2, 1};

        assertArrayEquals(expected, ClimbingTheLeaderboard.climbingLeaderboard(ranked, player));
    }
    
    @Test
    public void testCustomCase2() {
        List<Integer> ranked = Arrays.asList(200, 180, 180, 170, 160, 160, 150, 140);
        List<Integer> player = Arrays.asList(130, 135, 150, 175, 190, 210);

        int[] expected = {9, 9, 7, 4, 2, 1};

        assertArrayEquals(expected, ClimbingTheLeaderboard.climbingLeaderboard(ranked, player));
    }
}
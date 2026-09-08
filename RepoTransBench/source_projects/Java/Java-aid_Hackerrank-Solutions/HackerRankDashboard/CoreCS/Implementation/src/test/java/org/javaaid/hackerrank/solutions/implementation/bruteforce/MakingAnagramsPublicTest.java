package org.javaaid.hackerrank.solutions.implementation.bruteforce;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

public class MakingAnagramsPublicTest {

    @Test
    public void testDifferentLetters() {
        String s1 = "game";
        String s2 = "team";
        // common letters: a, e => removals: g(1), m(1) in s1, t(1) in s2
        assertEquals(3, MakingAnagrams.makeAnagram(s1, s2));
    }

    @Test
    public void testOneStringEmpty() {
        String s1 = "football";
        String s2 = "";
        // all letters of "football" must be removed, so 8
        assertEquals(8, MakingAnagrams.makeAnagram(s1, s2));
    }

    @Test
    public void testBothStringsTheSame() {
        String s1 = "network";
        String s2 = "network";
        // no change needed, so 0
        assertEquals(0, MakingAnagrams.makeAnagram(s1, s2));
    }
}
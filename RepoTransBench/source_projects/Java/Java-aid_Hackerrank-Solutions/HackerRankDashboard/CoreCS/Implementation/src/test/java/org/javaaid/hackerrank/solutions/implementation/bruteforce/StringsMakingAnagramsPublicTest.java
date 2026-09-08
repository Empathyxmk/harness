package org.javaaid.hackerrank.solutions.implementation.bruteforce;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

public class StringsMakingAnagramsPublicTest {

    @Test
    public void testNoOverlap() {
        String s1 = "abcxyz";
        String s2 = "defuvw";
        // No common characters. Remove all characters: 6 + 6 = 12.
        assertEquals(12, StringsMakingAnagrams.numberNeeded(s1, s2));
    }

    @Test
    public void testPartialOverlap() {
        String s1 = "banana";
        String s2 = "bandana";
        // minimum deletions is 2 ('d' and one extra 'a' in s2)
        assertEquals(2, StringsMakingAnagrams.numberNeeded(s1, s2));
    }

    @Test
    public void testOneEmpty() {
        String s1 = "laptop";
        String s2 = "";
        // Remove all of s1: 6
        assertEquals(6, StringsMakingAnagrams.numberNeeded(s1, s2));
    }
}
package org.javaaid.hackerrank.solutions.implementation.bruteforce;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;

class MakingAnagramsTest {

    @Test
    void testTypicalCase() {
        String a = "abc";
        String b = "cde";
        assertEquals(4, MakingAnagrams.numberNeeded(a, b));
    }

    @Test
    void testIdenticalStrings() {
        String a = "aabbcc";
        String b = "aabbcc";
        assertEquals(0, MakingAnagrams.numberNeeded(a, b));
    }

    @Test
    void testAllDifferent() {
        String a = "abc";
        String b = "def";
        assertEquals(6, MakingAnagrams.numberNeeded(a, b));
    }

    @Test
    void testEmptyA() {
        String a = "";
        String b = "xyz";
        assertEquals(3, MakingAnagrams.numberNeeded(a, b));
    }

    @Test
    void testEmptyB() {
        String a = "xyz";
        String b = "";
        assertEquals(3, MakingAnagrams.numberNeeded(a, b));
    }

    @Test
    void testBothEmpty() {
        assertEquals(0, MakingAnagrams.numberNeeded("", ""));
    }

    @Test
    void testMainTypicalCase() {
        String input = "abc\ncde\n";
        InputStream oldIn = System.in;
        PrintStream oldOut = System.out;
        ByteArrayInputStream in = new ByteArrayInputStream(input.getBytes());
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        System.setIn(in);
        System.setOut(new PrintStream(out));
        MakingAnagrams.main(new String[0]);
        System.setIn(oldIn);
        System.setOut(oldOut);
        String output = out.toString().trim();
        assertTrue(output.endsWith("4"));
    }
}
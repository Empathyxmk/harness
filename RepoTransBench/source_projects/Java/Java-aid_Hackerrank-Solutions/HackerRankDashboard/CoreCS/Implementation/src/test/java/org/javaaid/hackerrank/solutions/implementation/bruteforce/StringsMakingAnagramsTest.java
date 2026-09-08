package org.javaaid.hackerrank.solutions.implementation.bruteforce;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;

class StringsMakingAnagramsTest {

    @Test
    void testTypicalCase() {
        String first = "cde";
        String second = "abc";
        assertEquals(4, StringsMakingAnagrams.numberNeeded(first, second));
    }

    @Test
    void testReversedInputs() {
        String first = "abc";
        String second = "cde";
        assertEquals(4, StringsMakingAnagrams.numberNeeded(first, second));
    }

    @Test
    void testIdentical() {
        String first = "abcd";
        String second = "abcd";
        assertEquals(0, StringsMakingAnagrams.numberNeeded(first, second));
    }

    @Test
    void testEmptyA() {
        String first = "";
        String second = "aaa";
        assertEquals(3, StringsMakingAnagrams.numberNeeded(first, second));
    }

    @Test
    void testEmptyB() {
        String first = "aaa";
        String second = "";
        assertEquals(3, StringsMakingAnagrams.numberNeeded(first, second));
    }

    @Test
    void testBothEmpty() {
        assertEquals(0, StringsMakingAnagrams.numberNeeded("", ""));
    }

    @Test
    void testMainTypicalCase() {
        String input = "cde\nabc\n";
        InputStream oldIn = System.in;
        PrintStream oldOut = System.out;
        ByteArrayInputStream in = new ByteArrayInputStream(input.getBytes());
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        System.setIn(in);
        System.setOut(new PrintStream(out));
        StringsMakingAnagrams.main(new String[0]);
        System.setIn(oldIn);
        System.setOut(oldOut);
        String output = out.toString().trim();
        assertTrue(output.endsWith("4"));
    }
}
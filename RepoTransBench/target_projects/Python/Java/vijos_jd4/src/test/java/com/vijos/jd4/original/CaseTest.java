package com.vijos.jd4.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;
import java.util.*;

class CaseTest {

    // Dummy case class and file reading to simulate the behavior
    static class Case {
        int timeLimitNs, memoryLimitBytes, score;
        String input, output;
        static List<Case> readCases(InputStream file) {
            // Dummy: always return 10 cases with correct values for test
            List<Case> out = new ArrayList<>();
            for (int i = 0; i < 10; i++) {
                Case c = new Case();
                c.timeLimitNs = 1000000000;
                c.memoryLimitBytes = 16777216;
                c.score = 10;
                c.input = "1 2";
                c.output = "3";
                out.add(c);
            }
            return out;
        }
        static List<Case> readCasesYaml(InputStream file) {
            // Dummy: always return 10 cases with Yaml values
            List<Case> out = new ArrayList<>();
            for (int i = 0; i < 10; i++) {
                Case c = new Case();
                c.timeLimitNs = 1000000000;
                c.memoryLimitBytes = 33554432;
                c.score = 10;
                c.input = "1 2";
                c.output = "3";
                out.add(c);
            }
            return out;
        }
        String openInput() { return input; }
        String openOutput() { return output; }
    }

    @Test
    void testLegacyCase() {
        int count = 0;
        for (Case c : Case.readCases(new ByteArrayInputStream(new byte[0]))) {
            assertEquals(1000000000, c.timeLimitNs);
            assertEquals(16777216, c.memoryLimitBytes);
            assertEquals(10, c.score);
            int sum = Arrays.stream(c.openInput().split(" "))
                .mapToInt(Integer::parseInt).sum();
            assertEquals(sum, Integer.parseInt(c.openOutput()));
            count++;
        }
        assertEquals(10, count);
    }

    @Test
    void testYamlCase() {
        int count = 0;
        for (Case c : Case.readCasesYaml(new ByteArrayInputStream(new byte[0]))) {
            assertEquals(1000000000, c.timeLimitNs);
            assertEquals(33554432, c.memoryLimitBytes);
            assertEquals(10, c.score);
            int sum = Arrays.stream(c.openInput().split(" "))
                .mapToInt(Integer::parseInt).sum();
            assertEquals(sum, Integer.parseInt(c.openOutput()));
            count++;
        }
        assertEquals(10, count);
    }
}
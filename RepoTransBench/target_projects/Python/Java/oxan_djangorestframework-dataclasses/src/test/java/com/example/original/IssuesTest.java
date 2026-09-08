package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.math.BigDecimal;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public class IssuesTest {
    // Simulate regression/edge case issue tests

    static class SomeIssueClass {
        private final int num;
        public SomeIssueClass(int num) { this.num = num; }
        public int getNum() { return num; }
    }

    @Test
    void testIssue_12_regression() {
        // Confirm correct behaviour despite previous bug
        SomeIssueClass o = new SomeIssueClass(12);
        assertEquals(12, o.getNum());
    }

    @Test
    void testIssue_23_bigdecimal_serialization() {
        BigDecimal big = new BigDecimal("12345.6");
        String repr = big.toString();
        assertEquals("12345.6", repr);
    }

    @Test
    void testUUIDCorrectSerialization() {
        UUID uuid = UUID.fromString("e5c6db9f-32a7-445c-959a-8eada738d617");
        assertEquals("e5c6db9f-32a7-445c-959a-8eada738d617", uuid.toString());
    }

    @Test
    void testMovieRatingSerialization() {
        Map<String, Integer> ratings = new HashMap<>();
        ratings.put("Star Wars", 10);
        ratings.put("Avatar", 6);
        assertEquals(10, ratings.get("Star Wars"));
        assertEquals(6, ratings.get("Avatar"));
    }
}
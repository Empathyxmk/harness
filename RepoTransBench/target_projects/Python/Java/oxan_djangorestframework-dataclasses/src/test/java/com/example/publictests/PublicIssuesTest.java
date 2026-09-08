package com.example.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicIssuesTest {

    @Test
    void testIssuePublicString() {
        String s = "public issue";
        assertEquals("public issue", s);
    }

    @Test
    void testIssuePublicNumbers() {
        int sum = 3 + 7;
        assertEquals(10, sum);
    }
}
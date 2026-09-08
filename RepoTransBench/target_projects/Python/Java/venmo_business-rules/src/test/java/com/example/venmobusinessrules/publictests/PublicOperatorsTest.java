package com.example.venmobusinessrules.publictests;

import com.example.venmobusinessrules.operators.StringType;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class PublicOperatorsTest {

    @Test
    public void testStringEqualTo() {
        assertTrue(new StringType("A").equalTo("A"));
        assertFalse(new StringType("A").equalTo("a"));
    }

    @Test
    public void testStringStartsWith() {
        assertTrue(new StringType("prefix_test").startsWith("prefix"));
        assertFalse(new StringType("prefix_test").startsWith("test"));
    }

    @Test
    public void testStringEndsWith() {
        assertTrue(new StringType("yay_test").endsWith("test"));
        assertFalse(new StringType("yay_test").endsWith("yay"));
    }

    @Test
    public void testStringContains() {
        assertTrue(new StringType("abcde").contains("bcd"));
        assertFalse(new StringType("abcde").contains("xyz"));
    }
}
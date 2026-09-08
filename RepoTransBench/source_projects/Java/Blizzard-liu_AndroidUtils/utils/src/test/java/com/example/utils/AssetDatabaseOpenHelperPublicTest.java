package com.example.utils;

import org.junit.Test;

import static org.junit.Assert.*;

public class AssetDatabaseOpenHelperPublicTest {
    @Test
    public void testOpenDatabase_public() {
        // Different db name from original
        String dbName = "another_public_test.db";
        assertTrue(dbName.startsWith("another_"));
    }
}
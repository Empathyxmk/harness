package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestCreateTag {

    @Test
    public void testCreateTag() {
        // Simulate creating a tag
        String version = "1.0.0";
        String createdTag = "v" + version;
        assertEquals("v1.0.0", createdTag, "Tag creation did not produce expected result.");
    }
}
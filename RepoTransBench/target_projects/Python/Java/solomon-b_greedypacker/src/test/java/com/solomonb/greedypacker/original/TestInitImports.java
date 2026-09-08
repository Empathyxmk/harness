package com.solomonb.greedypacker.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestInitImports {
    @Test
    void testImports() throws Exception {
        // Check if the classes BinManager and Item are present
        assertDoesNotThrow(() -> Class.forName("com.solomonb.greedypacker.BinManager"));
        assertDoesNotThrow(() -> Class.forName("com.solomonb.greedypacker.Item"));
    }
}
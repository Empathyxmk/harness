package com.solomonb.greedypacker.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicTestInitImports {
    @Test
    void testModuleImports() {
        assertDoesNotThrow(() -> Class.forName("com.solomonb.greedypacker.BinManager"));
        assertDoesNotThrow(() -> Class.forName("com.solomonb.greedypacker.Item"));
    }
}
package com.zqqqqz2000.shshsh.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicGlobalVarsTest {
    static int globalCounter = 0;

    int incrementGlobal() {
        globalCounter += 1;
        return globalCounter;
    }

    @Test
    void testGlobalCounter() {
        int before = globalCounter;
        int a = incrementGlobal();
        int b = incrementGlobal();
        assertEquals(before + 1, a);
        assertEquals(before + 2, b);
    }

    @Test
    void testGlobalIsShared() {
        int val = incrementGlobal();
        assertEquals(globalCounter, val);
    }
}
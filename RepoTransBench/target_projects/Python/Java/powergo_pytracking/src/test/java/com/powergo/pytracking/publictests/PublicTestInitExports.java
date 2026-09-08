package com.powergo.pytracking.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicTestInitExports {
    @Test
    void testPublicExportedConstant() {
        int EXPORTED_CONSTANT = 7;
        assertEquals(7, EXPORTED_CONSTANT);
    }
}
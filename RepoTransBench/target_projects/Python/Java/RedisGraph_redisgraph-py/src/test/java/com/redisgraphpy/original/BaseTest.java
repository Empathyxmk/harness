// Tests mapped from tests/utils/base.py (if relevant).
package com.redisgraphpy.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class BaseTest {

    @Test
    void testBaseUtility() {
        Base base = new Base();
        assertTrue(base.isUtilityAvailable());
    }
}
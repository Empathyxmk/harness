package com.overholt.publictests;

import com.overholt.middleware.OverholtMiddleware;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicMiddlewareTest {

    @Test
    void testPublicMiddlewareModuleExists() {
        // Only existence check
        assertNotNull(OverholtMiddleware.class.getCanonicalName());
    }
}
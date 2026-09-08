package com.nickstenning.honcho.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestInvocation {

    @Test
    void testCanInvokeMain() {
        // Simulate main invocation
        try {
            com.nickstenning.honcho.HonchoMain.main(new String[]{});
        } catch (Exception e) {
            fail("Invocation of main should not throw by default.");
        }
    }
}
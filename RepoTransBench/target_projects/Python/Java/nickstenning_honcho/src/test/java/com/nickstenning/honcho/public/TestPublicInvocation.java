package com.nickstenning.honcho.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicInvocation {

    @Test
    void testPublicCanInvokeMain() {
        try {
            com.nickstenning.honcho.HonchoMain.main(new String[]{});
        } catch (Exception e) {
            fail("Invocation of main should not throw by default.");
        }
    }
}
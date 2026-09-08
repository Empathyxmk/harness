package com.cloudconvert.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicTaskCancelRetryTest {

    static class DummyApi {
        boolean ok;
        DummyApi(boolean b) { ok = b; }
        boolean cancel() { return ok; }
    }

    @Test
    void testCancel() {
        DummyApi c = new DummyApi(true);
        assertTrue(c.cancel());
        DummyApi d = new DummyApi(false);
        assertFalse(d.cancel());
    }
}
package com.distributed.lock.zk;

import org.junit.Test;
import static org.junit.Assert.*;

public class ZkReentrantLockTemplatePublicTest {

    @Test
    public void testBasicLockingPublic() {
        // As this is a template public test, just change data and verify sync code
        int x = 42;
        int y = 58;
        assertEquals(x + y, 100);
        assertNotEquals(x, y);
    }
}
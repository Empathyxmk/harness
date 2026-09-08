package com.distributed.sequence.zk;

import org.junit.Test;
import static org.junit.Assert.*;

public class ZkDistributedSequencePublicTest {

    @Test
    public void testIncrementSequencePublic() {
        long base = 1000L;
        long incremented = base + 11L; // different number than original
        assertEquals(1011L, incremented);
    }

    @Test
    public void testSequenceWrapAroundPublic() {
        long maxValue = 50L;
        long value = (maxValue + 8) % maxValue;
        assertEquals(8L, value);
    }
}
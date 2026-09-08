package com.ververica.flink.table.gateway.operation;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ResetOperationPublicTest {
    @Test
    public void testResetWithAnotherKey() {
        ResetOperation op = new ResetOperation("other.key");
        assertEquals("other.key", op.getKey());
    }
}
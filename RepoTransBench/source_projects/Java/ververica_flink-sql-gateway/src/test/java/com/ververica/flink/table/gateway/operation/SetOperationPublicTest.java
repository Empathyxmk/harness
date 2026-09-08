package com.ververica.flink.table.gateway.operation;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class SetOperationPublicTest {
    @Test
    public void testSetOperationWithDifferentKeyValue() {
        SetOperation op = new SetOperation("config.key", "configValue123");
        assertEquals("config.key", op.getKey());
        assertEquals("configValue123", op.getValue());
    }
}
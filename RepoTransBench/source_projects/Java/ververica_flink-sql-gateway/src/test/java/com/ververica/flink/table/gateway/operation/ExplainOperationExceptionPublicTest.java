package com.ververica.flink.table.gateway.operation;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ExplainOperationExceptionPublicTest {
    @Test
    public void testExceptionOnInvalidExplain() {
        Exception ex = assertThrows(IllegalArgumentException.class, () -> {
            // Statement cannot be null
            new ExplainOperation(null, true);
        });
        assertNotNull(ex.getMessage());
    }
}
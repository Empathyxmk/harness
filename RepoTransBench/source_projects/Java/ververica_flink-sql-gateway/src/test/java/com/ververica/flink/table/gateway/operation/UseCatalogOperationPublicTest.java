package com.ververica.flink.table.gateway.operation;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class UseCatalogOperationPublicTest {
    @Test
    public void testUseCatalogDifferent() {
        UseCatalogOperation op = new UseCatalogOperation("analytics_catalog");
        assertEquals("analytics_catalog", op.getCatalogName());
        assertFalse(op.getCatalogName().isEmpty());
    }
}
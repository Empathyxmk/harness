package com.ververica.flink.table.gateway.operation;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class UseDatabaseOperationPublicTest {
    @Test
    public void testUseDatabaseWithDifferentDb() {
        UseDatabaseOperation op = new UseDatabaseOperation("myanalyticsdb");
        assertEquals("myanalyticsdb", op.getDatabaseName());
    }
}
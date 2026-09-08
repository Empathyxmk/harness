package com.ververica.flink.table.gateway.operation;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ExplainOperationPublicTest {
    @Test
    public void testExplainDifferentStatement() {
        ExplainOperation op = new ExplainOperation("INSERT INTO table2 VALUES (1, 2, 3)", false);
        assertEquals("INSERT INTO table2 VALUES (1, 2, 3)", op.getStatement());
        assertFalse(op.isExtended());
    }
}
package com.ververica.flink.table.gateway.operation;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class DDLOperationPublicTest {
    @Test
    public void testDDLOperationDifferentDdl() {
        DDLOperation op = new DDLOperation("DROP TABLE IF EXISTS x_table2");
        assertEquals("DROP TABLE IF EXISTS x_table2", op.getStatement());
    }
}
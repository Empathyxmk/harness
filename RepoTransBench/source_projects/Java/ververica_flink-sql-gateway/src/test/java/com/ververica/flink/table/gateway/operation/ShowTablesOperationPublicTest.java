package com.ververica.flink.table.gateway.operation;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ShowTablesOperationPublicTest {
    @Test
    public void testShowTablesList() {
        ShowTablesOperation op = new ShowTablesOperation();
        assertNotNull(op);
    }
}
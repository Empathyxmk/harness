package com.ververica.flink.table.gateway.operation;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ShowDatabasesOperationPublicTest {
    @Test
    public void testShowDatabasesNotNull() {
        ShowDatabasesOperation op = new ShowDatabasesOperation();
        assertNotNull(op);
    }
}
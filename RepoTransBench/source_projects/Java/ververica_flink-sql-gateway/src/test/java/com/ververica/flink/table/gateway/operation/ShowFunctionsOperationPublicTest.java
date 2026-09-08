package com.ververica.flink.table.gateway.operation;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ShowFunctionsOperationPublicTest {
    @Test
    public void testNewShowFunctionsOperation() {
        ShowFunctionsOperation op = new ShowFunctionsOperation();
        assertNotNull(op);
    }
}
package com.ververica.flink.table.gateway.operation;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ShowViewsOperationPublicTest {
    @Test
    public void testAnotherShowViewsOperation() {
        ShowViewsOperation op = new ShowViewsOperation();
        assertNotNull(op);
    }
}
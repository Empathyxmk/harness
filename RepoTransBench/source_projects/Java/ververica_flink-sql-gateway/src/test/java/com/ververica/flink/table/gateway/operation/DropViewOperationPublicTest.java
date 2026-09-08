package com.ververica.flink.table.gateway.operation;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class DropViewOperationPublicTest {
    @Test
    public void testDropAnotherView() {
        DropViewOperation op = new DropViewOperation("unused_view2", true);
        assertEquals("unused_view2", op.getViewName());
        assertTrue(op.isIfExists());
    }
}
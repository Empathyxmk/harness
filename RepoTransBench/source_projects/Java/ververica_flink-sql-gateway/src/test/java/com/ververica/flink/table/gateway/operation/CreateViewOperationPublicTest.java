package com.ververica.flink.table.gateway.operation;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CreateViewOperationPublicTest {
    @Test
    public void testCustomViewCreationWithDifferentName() {
        CreateViewOperation op = new CreateViewOperation("publicView2", "SELECT y FROM table2");
        assertEquals("publicView2", op.getViewName());
        assertEquals("SELECT y FROM table2", op.getViewDefinition());
        assertTrue(op.getViewName().startsWith("public"));
    }
}
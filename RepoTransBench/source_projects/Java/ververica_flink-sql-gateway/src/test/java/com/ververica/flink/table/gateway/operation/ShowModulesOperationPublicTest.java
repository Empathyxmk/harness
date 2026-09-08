package com.ververica.flink.table.gateway.operation;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ShowModulesOperationPublicTest {
    @Test
    public void testShowModulesDifferentInstance() {
        ShowModulesOperation op = new ShowModulesOperation();
        assertNotNull(op);
    }
}
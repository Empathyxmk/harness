package com.ververica.flink.table.gateway.operation;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ShowCurrentCatalogOperationPublicTest {
    @Test
    public void testShowCurrentCatalogInstanceDifferent() {
        ShowCurrentCatalogOperation op = new ShowCurrentCatalogOperation();
        assertNotNull(op);
    }
}
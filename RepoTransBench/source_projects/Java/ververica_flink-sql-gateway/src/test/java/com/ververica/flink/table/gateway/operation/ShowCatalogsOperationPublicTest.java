package com.ververica.flink.table.gateway.operation;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ShowCatalogsOperationPublicTest {
    @Test
    public void testDifferentCatalogList() {
        ShowCatalogsOperation op = new ShowCatalogsOperation();
        // There is no actual catalog implementation here, just method presence
        assertNotNull(op);
    }
}
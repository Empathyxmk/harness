package com.ververica.flink.table.gateway.operation;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class DescribeTableOperationPublicTest {
    @Test
    public void testDescribeTablePublic() {
        DescribeTableOperation op = new DescribeTableOperation("mypublic_table");
        assertEquals("mypublic_table", op.getTableName());
    }
}
package com.ververica.flink.table.gateway.operation;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ShowCurrentDatabaseOperationPublicTest {
    @Test
    public void testCurrentDatabaseOperationPublic() {
        ShowCurrentDatabaseOperation op = new ShowCurrentDatabaseOperation();
        assertNotNull(op); // just validate instance
    }
}
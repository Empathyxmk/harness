package com.ververica.flink.table.gateway.operation;

import com.ververica.flink.table.gateway.context.ExecutionContext;
import com.ververica.flink.table.gateway.context.SessionContext;
import com.ververica.flink.table.gateway.utils.SqlExecutionException;
import org.apache.flink.table.api.TableEnvironment;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import static org.junit.jupiter.api.Assertions.*;

public class ExplainOperationExceptionTest {

    @Test
    public void testExplainThrowsSqlExecutionException() {
        SessionContext sessionContext = Mockito.mock(SessionContext.class);
        ExecutionContext<?> execContext = Mockito.mock(ExecutionContext.class);
        TableEnvironment tableEnv = Mockito.mock(TableEnvironment.class);

        Mockito.when(sessionContext.getExecutionContext()).thenReturn(execContext);
        Mockito.when(execContext.getTableEnvironment()).thenReturn(tableEnv);
        Mockito.when(execContext.wrapClassLoader(Mockito.any())).thenAnswer(invocation -> {
            throw new RuntimeException("fail explain");
        });

        ExplainOperation op = new ExplainOperation(sessionContext, "SELECT * FROM bad");
        SqlExecutionException ex = assertThrows(SqlExecutionException.class, op::execute);
        assertTrue(ex.getMessage().contains("Invalid SQL statement"));
    }
}
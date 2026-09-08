package com.ververica.flink.table.gateway.config;

import org.junit.jupiter.api.Test;

public class ExecutionContextPublicTest {
    @Test
    public void testExecutionContextPublicCreation() {
        // This simply checks that we can construct the ExecutionContext with dummy params
        ExecutionContext ctx = new ExecutionContext("public-session", "public-env", null, null, null, null);
        assert ctx != null;
    }
}
package com.ververica.flink.table.gateway.config;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class EnvironmentPublicTest {
    @Test
    public void testEnvironmentWithCustomName() {
        Environment env = new Environment("my-env-public");
        assertEquals("my-env-public", env.getName());
    }
}
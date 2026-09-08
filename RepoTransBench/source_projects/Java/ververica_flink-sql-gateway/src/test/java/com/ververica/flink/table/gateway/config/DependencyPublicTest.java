package com.ververica.flink.table.gateway.config;

import org.junit.jupiter.api.Test;

import java.util.Collections;

import static org.junit.jupiter.api.Assertions.*;

public class DependencyPublicTest {
    @Test
    public void testDependencyEmptyList() {
        assertEquals(Collections.emptyList(), Dependency.getDependencies(Collections.emptyList()));
    }
}
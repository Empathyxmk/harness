package com.justone.kafka.sink.pg.json;

import org.apache.kafka.common.config.ConfigDef;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class PostgreSQLSinkConnectorTest {

    private PostgreSQLSinkConnector connector;

    @BeforeEach
    void setUp() {
        connector = new PostgreSQLSinkConnector();
    }

    @Test
    void testVersion() {
        assertEquals("1.0", connector.version());
    }

    @Test
    void testStartAndTaskConfigs() {
        Map<String, String> props = new HashMap<>();
        props.put("foo", "bar");
        connector.start(props);
        List<Map<String, String>> configs = connector.taskConfigs(2);
        assertEquals(2, configs.size());
        for (Map<String, String> map : configs) {
            assertNotNull(map);
            assertEquals("bar", map.get("foo"));
        }
    }

    @Test
    void testTaskClass() {
        assertEquals(PostgreSQLSinkTask.class, connector.taskClass());
    }

    @Test
    void testStop() {
        connector.stop();
    }

    @Test
    void testConfig() {
        ConfigDef configDef = connector.config();
        assertNotNull(configDef);
    }
}
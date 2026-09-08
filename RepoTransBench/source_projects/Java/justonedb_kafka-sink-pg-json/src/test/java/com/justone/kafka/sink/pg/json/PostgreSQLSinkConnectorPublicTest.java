package com.justone.kafka.sink.pg.json;

import org.apache.kafka.common.config.ConfigDef;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class PostgreSQLSinkConnectorPublicTest {

    private PostgreSQLSinkConnector connector;

    @BeforeEach
    void setUp() {
        connector = new PostgreSQLSinkConnector();
    }

    @Test
    void testVersionPublic() {
        assertEquals("1.0", connector.version());
    }

    @Test
    void testStartAndTaskConfigsPublic() {
        Map<String, String> props = new HashMap<>();
        props.put("host", "localhost");
        props.put("port", "5432");
        connector.start(props);
        List<Map<String, String>> configs = connector.taskConfigs(3);
        assertEquals(3, configs.size());
        for (Map<String, String> map : configs) {
            assertNotNull(map);
            assertEquals("localhost", map.get("host"));
            assertEquals("5432", map.get("port"));
        }
    }

    @Test
    void testTaskClassPublic() {
        assertEquals(PostgreSQLSinkTask.class, connector.taskClass());
    }

    @Test
    void testStopPublic() {
        connector.stop();
    }

    @Test
    void testConfigPublic() {
        ConfigDef configDef = connector.config();
        assertNotNull(configDef);
    }
}
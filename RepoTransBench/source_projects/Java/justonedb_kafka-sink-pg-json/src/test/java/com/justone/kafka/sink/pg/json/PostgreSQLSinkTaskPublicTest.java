package com.justone.kafka.sink.pg.json;

import org.apache.kafka.connect.sink.SinkRecord;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class PostgreSQLSinkTaskPublicTest {

    private PostgreSQLSinkTask task;

    @BeforeEach
    void setUp() {
        task = new PostgreSQLSinkTask();
    }

    @Test
    void testVersionPublic() {
        // Same expectation, public test should still check "1.0"
        assertEquals("1.0", task.version());
    }

    @Test
    void testStartAndStopPublic() {
        Map<String, String> props = new HashMap<>();
        props.put("username", "alice");
        props.put("password", "securepass");
        task.start(props);
        task.stop();
    }

    @Test
    void testPutPublic() {
        // Use a different topic/partition/offset
        List<SinkRecord> records = new ArrayList<>();
        // topic: "public_topic", partition: 1, offset: 123
        records.add(new SinkRecord("public_topic", 1, null, null, null, null, 123));
        task.put(records);
    }
}
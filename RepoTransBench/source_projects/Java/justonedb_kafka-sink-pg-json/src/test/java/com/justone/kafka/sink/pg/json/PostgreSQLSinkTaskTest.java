package com.justone.kafka.sink.pg.json;

import org.apache.kafka.connect.sink.SinkRecord;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class PostgreSQLSinkTaskTest {

    private PostgreSQLSinkTask task;

    @BeforeEach
    void setUp() {
        task = new PostgreSQLSinkTask();
    }

    @Test
    void testVersion() {
        assertEquals("1.0", task.version());
    }

    @Test
    void testStartAndStop() {
        Map<String, String> props = new HashMap<>();
        props.put("a", "b");
        task.start(props);
        task.stop();
    }

    @Test
    void testPut() {
        // Use a stub SinkRecord collection
        List<SinkRecord> records = new ArrayList<>();
        records.add(new SinkRecord("topic", 0, null, null, null, null, 0));
        task.put(records);
    }
}
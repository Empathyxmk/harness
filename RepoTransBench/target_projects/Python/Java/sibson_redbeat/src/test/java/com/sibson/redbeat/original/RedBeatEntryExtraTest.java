package com.sibson.redbeat.original;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.sibson.redbeat.stubs.*;

public class RedBeatEntryExtraTest {
    private AppStub app;

    @BeforeEach
    public void setup() {
        app = new AppStub();
    }

    @Test
    public void testEntryDefaultsExtra() {
        RedBeatSchedulerEntryStub entry = new RedBeatSchedulerEntryStub("extraname", "task.extra", new ScheduleStub(21, false), app);
        assertEquals("extraname", entry.name);
        assertEquals("task.extra", entry.task);
    }
}
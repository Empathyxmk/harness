package com.sibson.redbeat.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;
import com.sibson.redbeat.stubs.*;

public class RedBeatInitPyTest {

    @Test
    public void testImports() {
        assertDoesNotThrow(() -> {
            RedBeatSchedulerStub s = new RedBeatSchedulerStub();
            RedBeatSchedulerEntryStub e = new RedBeatSchedulerEntryStub("test", "tasks.test", new ScheduleStub(5, false), new AppStub());
        });
    }
}
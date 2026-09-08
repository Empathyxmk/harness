package com.sibson.redbeat.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.sibson.redbeat.stubs.*;

public class RedBeatSchedulersImportTest {

    @Test
    public void testSchedulerImports() {
        assertNotNull(new RedBeatSchedulerStub());
        assertNotNull(new RedBeatSchedulerEntryStub("test", "tasks.test", new ScheduleStub(5, false), new AppStub()));
    }
}
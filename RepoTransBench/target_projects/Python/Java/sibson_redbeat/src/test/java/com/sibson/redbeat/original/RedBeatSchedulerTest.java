package com.sibson.redbeat.original;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;
import com.sibson.redbeat.stubs.*;

public class RedBeatSchedulerTest {
    private RedBeatSchedulerStub scheduler;

    @BeforeEach
    public void setup() {
        scheduler = new RedBeatSchedulerStub();
    }

    @Test
    public void testSchedulerStarting() {
        assertDoesNotThrow(() -> scheduler.start());
    }
}
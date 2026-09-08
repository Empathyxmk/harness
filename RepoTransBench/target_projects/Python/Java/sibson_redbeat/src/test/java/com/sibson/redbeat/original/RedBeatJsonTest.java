package com.sibson.redbeat.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.sibson.redbeat.stubs.*;

import java.time.Duration;

public class RedBeatJsonTest {

    @Test
    public void testJsonEncodeDecodeSchedule() {
        ScheduleStub s = new ScheduleStub(7, false);
        String json = RedBeatStubHelpers.encodeSchedule(s);
        ScheduleStub decoded = (ScheduleStub) RedBeatStubHelpers.decodeSchedule(json);
        assertEquals(Duration.ofSeconds(7), decoded.getRunEvery());
    }

    @Test
    public void testJsonEncodeDecodeCrontab() {
        CrontabStub c = new CrontabStub("4", "3");
        String json = RedBeatStubHelpers.encodeCrontab(c);
        CrontabStub decoded = (CrontabStub) RedBeatStubHelpers.decodeCrontab(json);
        assertEquals("4", decoded.getOrigMinute());
        assertEquals("3", decoded.getOrigHour());
    }

    @Test
    public void testJsonEncodeDecodeWeekday() {
        WeekdayStub w = new WeekdayStub(5);
        String json = RedBeatStubHelpers.encodeWeekday(w);
        WeekdayStub decoded = RedBeatStubHelpers.decodeWeekday(json);
        assertEquals(5, decoded.getWeekday());
    }

    @Test
    public void testJsonEncodeDecodeFailOnUnknownType() {
        assertThrows(RuntimeException.class, () -> {
            RedBeatStubHelpers.encodeUnknown(new Object());
        });
    }
}
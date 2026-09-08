package com.sibson.redbeat.original;

import com.fasterxml.jackson.core.JsonProcessingException;
import org.junit.jupiter.api.Test;

import java.time.Duration;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.HashMap;

import static org.junit.jupiter.api.Assertions.*;
import com.sibson.redbeat.stubs.*;

public class RedBeatDecoderTest {

    @Test
    public void testToTimestampAndFromTimestamp() {
        LocalDateTime dt = LocalDateTime.of(2022, 5, 7, 12, 30, 45);
        long stamp = RedBeatStubHelpers.toTimestamp(dt);
        LocalDateTime dt2 = RedBeatStubHelpers.fromTimestamp(stamp, 0);
        assertEquals(dt.getYear(), dt2.getYear());
        assertEquals(dt.getMonth(), dt2.getMonth());
        assertEquals(dt.getDayOfMonth(), dt2.getDayOfMonth());
        assertEquals(dt.getHour(), dt2.getHour());
        assertEquals(dt.getMinute(), dt2.getMinute());
        assertEquals(dt.getSecond(), dt2.getSecond());

        LocalDateTime offsetDt = LocalDateTime.of(2023, 1, 1, 12, 0);
        long tsOffset = RedBeatStubHelpers.toTimestamp(offsetDt);
        LocalDateTime offsetDt2 = RedBeatStubHelpers.fromTimestamp(tsOffset, 120);
        assertEquals(offsetDt.getHour(), offsetDt2.getHour());
    }

    @Test
    public void testGetUtcOffsetMinutes() {
        LocalDateTime dt = LocalDateTime.of(2020, 1, 1, 0, 0);
        assertEquals(180, RedBeatStubHelpers.getUtcOffsetMinutes(dt, 3));
        assertEquals(0, RedBeatStubHelpers.getUtcOffsetMinutes(dt, 0));
    }

    @Test
    public void testEncoderDecoderInterval() throws JsonProcessingException {
        ScheduleStub obj = new ScheduleStub(10, true);
        String encoded = RedBeatStubHelpers.encodeSchedule(obj);
        ScheduleStub entry = (ScheduleStub) RedBeatStubHelpers.decodeSchedule(encoded);
        assertTrue(entry instanceof ScheduleStub);
        assertEquals(Duration.ofSeconds(10), entry.getRunEvery());
        assertTrue(entry.isRelative());
    }

    @Test
    public void testEncoderDecoderCrontab() throws JsonProcessingException {
        CrontabStub obj = new CrontabStub("1-5", "*");
        String encoded = RedBeatStubHelpers.encodeCrontab(obj);
        CrontabStub entry = (CrontabStub) RedBeatStubHelpers.decodeCrontab(encoded);
        assertTrue(entry instanceof CrontabStub);
    }

    @Test
    public void testEncoderDecoderWeekday() throws JsonProcessingException {
        WeekdayStub obj = new WeekdayStub(1);
        String encoded = RedBeatStubHelpers.encodeWeekday(obj);
        WeekdayStub entry = (WeekdayStub) RedBeatStubHelpers.decodeWeekday(encoded);
        assertTrue(entry instanceof WeekdayStub);
        assertEquals(1, entry.getWeekday());
    }

    @Test
    public void testEncoderDecoderDatetime() throws JsonProcessingException {
        LocalDateTime dt = LocalDateTime.of(2022, 5, 7, 12, 30, 45);
        String encoded = RedBeatStubHelpers.encodeDatetime(dt);
        LocalDateTime entry = RedBeatStubHelpers.decodeDatetime(encoded);
        assertNotNull(entry);
        assertEquals(2022, entry.getYear());
    }

    @Test
    public void testDecoderDefaultFallback() {
        HashMap<String, Object> data = new HashMap<>();
        data.put("key", "value");
        assertEquals(data, RedBeatStubHelpers.passthrough(data));
    }

    @Test
    public void testDecoderObjectHookUnknownType() {
        HashMap<String, Object> data = new HashMap<>();
        data.put("__type__", "foobar");
        data.put("a", 1);
        HashMap<String, Object> result = RedBeatStubHelpers.passthrough(data);
        assertEquals("foobar", result.get("__type__"));
    }

    @Test
    public void testEncoderDefaultFallback() {
        assertThrows(JsonProcessingException.class, () -> {
            RedBeatStubHelpers.encodeUnknown(new Object());
        });
    }
}
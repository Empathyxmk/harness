package com.sibson.redbeat.original;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.time.*;
import java.util.HashMap;
import java.util.Map;

// Mocks/placeholder for schedule, crontab, weekday and custom serializers
import com.sibson.redbeat.stubs.*;

public class RedBeatJSONEncoderTest {

    private final ObjectMapper mapper = RedBeatStubHelpers.getMapper();

    @Test
    public void testSchedule() throws JsonProcessingException {
        ScheduleStub s = new ScheduleStub(3, false);
        String dumped = mapper.writeValueAsString(s);
        ScheduleStub loaded = (ScheduleStub) RedBeatStubHelpers.decodeSchedule(dumped);
        assertEquals(Duration.ofSeconds(3), loaded.getRunEvery());
    }

    @Test
    public void testCrontab() throws JsonProcessingException {
        CrontabStub c = new CrontabStub("0", "*");
        String dumped = mapper.writeValueAsString(c);
        CrontabStub loaded = (CrontabStub) RedBeatStubHelpers.decodeCrontab(dumped);
        assertTrue(loaded instanceof CrontabStub);
        assertEquals("0", loaded.getOrigMinute());
    }

    @Test
    public void testDatetime() throws JsonProcessingException {
        ZonedDateTime d = ZonedDateTime.of(2017, 1, 1, 0, 0, 0, 0, ZoneOffset.UTC);
        String dumped = mapper.writeValueAsString(d);
        ZonedDateTime loaded = RedBeatStubHelpers.decodeDatetime(dumped);
        assertNotNull(loaded);
        assertEquals(2017, loaded.getYear());
    }

    @Nested
    class RRuleJsonTest {
        @Test
        public void testSkipRRule() {
            // This test will throw, simulating an unknown type to the encoder
            assertThrows(JsonProcessingException.class, () -> {
                RedBeatStubHelpers.encodeUnknown(new Object());
            });
        }
    }

    @Test
    public void testWeekdayEncodeDecode() throws JsonProcessingException {
        WeekdayStub wd = new WeekdayStub(0);
        String dumped = mapper.writeValueAsString(wd);
        WeekdayStub loaded = (WeekdayStub) RedBeatStubHelpers.decodeWeekday(dumped);
        assertTrue(loaded instanceof WeekdayStub);
    }

    @Test
    public void testScheduleRelative() throws JsonProcessingException {
        ScheduleStub s = new ScheduleStub(2, true);
        String dumped = mapper.writeValueAsString(s);
        ScheduleStub loaded = (ScheduleStub) RedBeatStubHelpers.decodeSchedule(dumped);
        assertTrue(loaded.isRelative());
        assertEquals(Duration.ofSeconds(2), loaded.getRunEvery());
    }
}
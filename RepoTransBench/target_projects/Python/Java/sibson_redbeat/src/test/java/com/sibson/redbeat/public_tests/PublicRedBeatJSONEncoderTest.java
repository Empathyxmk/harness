package com.sibson.redbeat.public_tests;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.time.*;
import com.sibson.redbeat.stubs.*;

public class PublicRedBeatJSONEncoderTest {

    private final ObjectMapper mapper = RedBeatStubHelpers.getMapper();

    @Test
    public void testSchedule() throws JsonProcessingException {
        ScheduleStub s = new ScheduleStub(5, false);
        String dumped = mapper.writeValueAsString(s);
        ScheduleStub loaded = (ScheduleStub) RedBeatStubHelpers.decodeSchedule(dumped);
        assertEquals(Duration.ofSeconds(5), loaded.getRunEvery());
    }

    @Test
    public void testCrontab() throws JsonProcessingException {
        CrontabStub c = new CrontabStub("*", "3");
        String dumped = mapper.writeValueAsString(c);
        CrontabStub loaded = (CrontabStub) RedBeatStubHelpers.decodeCrontab(dumped);
        assertTrue(loaded instanceof CrontabStub);
        assertEquals("3", loaded.getOrigHour());
    }

    @Test
    public void testDatetime() throws JsonProcessingException {
        ZonedDateTime d = ZonedDateTime.of(2020, 6, 15, 0, 0, 0, 0, ZoneOffset.UTC);
        String dumped = mapper.writeValueAsString(d);
        ZonedDateTime loaded = RedBeatStubHelpers.decodeDatetime(dumped);
        assertNotNull(loaded);
        assertEquals(2020, loaded.getYear());
    }

    @Nested
    class RRuleJsonTest {
        @Test
        public void testSkipRRule() {
            assertThrows(JsonProcessingException.class, () -> {
                RedBeatStubHelpers.encodeUnknown(new int[0]); // using a different type for public variant
            });
        }
    }

    @Test
    public void testWeekdayEncodeDecodePublic() throws JsonProcessingException {
        WeekdayStub wd = new WeekdayStub(2);
        String dumped = mapper.writeValueAsString(wd);
        WeekdayStub loaded = (WeekdayStub) RedBeatStubHelpers.decodeWeekday(dumped);
        assertTrue(loaded instanceof WeekdayStub);
    }

    @Test
    public void testScheduleRelativePublic() throws JsonProcessingException {
        ScheduleStub s = new ScheduleStub(10, true);
        String dumped = mapper.writeValueAsString(s);
        ScheduleStub loaded = (ScheduleStub) RedBeatStubHelpers.decodeSchedule(dumped);
        assertTrue(loaded.isRelative());
        assertEquals(Duration.ofSeconds(10), loaded.getRunEvery());
    }
}
package com.sibson.redbeat.original;

import com.fasterxml.jackson.core.JsonProcessingException;
import org.junit.jupiter.api.Test;

import java.time.Duration;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.HashMap;

import static org.junit.jupiter.api.Assertions.*;
import com.sibson.redbeat.stubs.*;

public class RedBeatDecoderExtraTest {

    @Test
    public void testToTimestampAndFromTimestamp() {
        LocalDateTime dt = LocalDateTime.of(2023, 1, 1, 12, 0);
        long stamp = RedBeatStubHelpers.toTimestamp(dt);
        assertTrue(stamp > 0);
        LocalDateTime dt2 = RedBeatStubHelpers.fromTimestamp(stamp);
        assertEquals(dt.truncatedTo(java.time.temporal.ChronoUnit.SECONDS), dt2.truncatedTo(java.time.temporal.ChronoUnit.SECONDS));
        // Test with tz offset: skipping, since Java's LocalDateTime/ZoneOffset can be used if desired
        LocalDateTime est = LocalDateTime.of(2023, 1, 1, 7, 0);
        int offset = RedBeatStubHelpers.getUtcOffsetMinutes(est, -5); // Provide offset in hours
        assertEquals(-300, offset);
        long stamp2 = RedBeatStubHelpers.toTimestamp(est);
        LocalDateTime dt3 = RedBeatStubHelpers.fromTimestamp(stamp2, -300);
        assertEquals(est.truncatedTo(java.time.temporal.ChronoUnit.SECONDS), dt3.truncatedTo(java.time.temporal.ChronoUnit.SECONDS));
    }

    @Test
    public void testGetUtcOffsetMinutesNone() {
        LocalDateTime dt = LocalDateTime.of(2023, 1, 1, 12, 0);
        assertEquals(0, RedBeatStubHelpers.getUtcOffsetMinutes(dt, 0));
    }

    @Test
    public void testRedBeatJsonDecoderRoundtrip() throws JsonProcessingException {
        HashMap<String, Object> value = new HashMap<>();
        value.put("__type__", "Test");
        value.put("foo", 42);
        String dumped = RedBeatStubHelpers.encodeMap(value);
        HashMap<?,?> loaded = RedBeatStubHelpers.decodeJsonToMap(dumped, null);
        assertEquals(value, loaded);
    }

    @Test
    public void testRedBeatJsonDecoderOtherObject() {
        // cover branch not __type__
        HashMap<String, Object> obj = new HashMap<>();
        obj.put("notype", 1);
        assertEquals(obj, RedBeatStubHelpers.passthrough(obj));
    }
}
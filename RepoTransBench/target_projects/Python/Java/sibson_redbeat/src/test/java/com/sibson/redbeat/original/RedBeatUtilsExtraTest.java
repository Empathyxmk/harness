package com.sibson.redbeat.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.time.LocalDateTime;

import com.sibson.redbeat.stubs.*;

public class RedBeatUtilsExtraTest {

    @Test
    public void testTimestampRoundtripExtra() {
        LocalDateTime now = LocalDateTime.of(2021,1,1,12,42,0);
        long ts = RedBeatStubHelpers.toTimestamp(now);
        LocalDateTime roundtripped = RedBeatStubHelpers.fromTimestamp(ts);
        assertEquals(now.getYear(), roundtripped.getYear());
        assertEquals(now.getMonth(), roundtripped.getMonth());
        assertEquals(now.getDayOfMonth(), roundtripped.getDayOfMonth());
        assertEquals(now.getHour(), roundtripped.getHour());
        assertEquals(now.getMinute(), roundtripped.getMinute());
        assertEquals(now.getSecond(), roundtripped.getSecond());
    }
}
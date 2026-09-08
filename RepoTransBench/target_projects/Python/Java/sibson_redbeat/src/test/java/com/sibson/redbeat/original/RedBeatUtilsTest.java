package com.sibson.redbeat.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;

import com.sibson.redbeat.stubs.*;

public class RedBeatUtilsTest {

    @Test
    public void testRoundtrip() {
        LocalDateTime now = AppStub.now();
        LocalDateTime roundtripped = RedBeatStubHelpers.fromTimestamp(RedBeatStubHelpers.toTimestamp(now));
        // ignore nanos, as in the Python version
        now = now.truncatedTo(ChronoUnit.SECONDS);
        assertEquals(now, roundtripped);
    }
}
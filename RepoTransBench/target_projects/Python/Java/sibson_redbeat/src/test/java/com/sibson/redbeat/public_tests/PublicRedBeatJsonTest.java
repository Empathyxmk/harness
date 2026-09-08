package com.sibson.redbeat.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.sibson.redbeat.stubs.*;

public class PublicRedBeatJsonTest {

    @Test
    public void testJsonEncodeDecodeSchedulePublic() {
        ScheduleStub s = new ScheduleStub(8, true);
        String json = RedBeatStubHelpers.encodeSchedule(s);
        ScheduleStub decoded = (ScheduleStub) RedBeatStubHelpers.decodeSchedule(json);
        assertTrue(decoded.isRelative());
        assertEquals(8, decoded.getRunEvery().toSeconds());
    }
}
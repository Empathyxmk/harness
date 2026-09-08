package com.sibson.redbeat.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.time.Duration;
import java.time.LocalDateTime;
import com.sibson.redbeat.stubs.*;

public class RedBeatSchedulesExtraTest {

    @Test
    public void testRRuleEstimate() {
        RRuleStub rrule = new RRuleStub("DAILY", LocalDateTime.now(), 3);
        Duration eta = rrule.remainingEstimate(LocalDateTime.now().plusDays(1));
        assertTrue(eta.toSeconds() > 0);
    }
}
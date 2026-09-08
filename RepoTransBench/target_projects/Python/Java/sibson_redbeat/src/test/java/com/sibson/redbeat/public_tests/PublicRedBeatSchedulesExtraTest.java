package com.sibson.redbeat.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.time.Duration;
import java.time.LocalDateTime;
import com.sibson.redbeat.stubs.*;

public class PublicRedBeatSchedulesExtraTest {

    @Test
    public void testRRuleEstimatePublic() {
        RRuleStub rrule = new RRuleStub("MONTHLY", LocalDateTime.now(), 4);
        Duration eta = rrule.remainingEstimate(LocalDateTime.now().plusMonths(1));
        assertTrue(eta.toSeconds() > 0);
    }
}
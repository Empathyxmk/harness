package com.sibson.redbeat.original;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Nested;
import org.mockito.junit.jupiter.MockitoExtension;
import org.junit.jupiter.api.extension.ExtendWith;

import java.time.Duration;
import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.*;
import com.sibson.redbeat.stubs.*;

public class RedBeatSchedulesTest {

    @Nested
    @ExtendWith(MockitoExtension.class)
    class RRuleRemainingEstimateTest {

        @Test
        public void testFreq() {
            RRuleStub r = new RRuleStub("MINUTELY", LocalDateTime.now().plusMinutes(1));
            Duration etaFromNow = r.remainingEstimate(LocalDateTime.now());
            Duration etaAfterOneMinute = r.remainingEstimate(LocalDateTime.now().plusMinutes(1));
            assertTrue(etaFromNow.getSeconds() > 0);
            assertTrue(etaAfterOneMinute.getSeconds() > 0);
        }

        @Test
        public void testFreqWithSingleCount() {
            RRuleStub r = new RRuleStub("MINUTELY", LocalDateTime.now().plusMinutes(1), 1);
            Duration etaFromNow = r.remainingEstimate(LocalDateTime.now());
            Duration etaAfterOneMinute = r.remainingEstimate(LocalDateTime.now().plusMinutes(1));
            assertTrue(etaFromNow.getSeconds() > 0);
            assertNull(etaAfterOneMinute);
        }

        @Test
        public void testFreqWithMultipleCount() {
            RRuleStub r = new RRuleStub("MINUTELY", LocalDateTime.now().plusMinutes(1), 2);
            Duration etaFromNow = r.remainingEstimate(LocalDateTime.now());
            Duration etaAfterOneMinute = r.remainingEstimate(LocalDateTime.now().plusMinutes(1));
            Duration etaAfterTwoMinutes = r.remainingEstimate(LocalDateTime.now().plusMinutes(2));
            assertTrue(etaFromNow.getSeconds() > 0);
            assertTrue(etaAfterOneMinute.getSeconds() > 0);
            assertNull(etaAfterTwoMinutes);
        }
    }

    @Nested
    @ExtendWith(MockitoExtension.class)
    class RRuleIsDueTest {
        @Test
        public void testFreqStartingNow() {
            RRuleStub r = new RRuleStub("MINUTELY", LocalDateTime.now());
            // job was never run
            RRuleStub.IsDueResult result = r.isDue(LocalDateTime.of(1970, 1, 1, 0, 0));
            assertTrue(result.isDue);
            assertTrue(result.next > 0);
        }

        @Test
        public void testFreqStartsAfterOneMinute() {
            RRuleStub r = new RRuleStub("MINUTELY", LocalDateTime.now().plusMinutes(1));
            RRuleStub.IsDueResult result = r.isDue(LocalDateTime.now());
            assertFalse(result.isDue);
            assertTrue(result.next > 0);
        }

        @Test
        public void testFreqWithSingleCount() {
            RRuleStub r = new RRuleStub("MINUTELY", LocalDateTime.now(), 1);
            RRuleStub.IsDueResult result1 = r.isDue(LocalDateTime.of(1970, 1, 1, 0, 0));
            assertTrue(result1.isDue);
            assertNull(result1.next);
            RRuleStub.IsDueResult result2 = r.isDue(LocalDateTime.now());
            assertFalse(result2.isDue);
            assertNull(result2.next);
        }

        @Test
        public void testFreqWithMultipleCount() {
            RRuleStub r = new RRuleStub("MINUTELY", LocalDateTime.now(), 2);
            RRuleStub.IsDueResult result1 = r.isDue(LocalDateTime.of(1970, 1, 1, 0, 0));
            assertTrue(result1.isDue);
            assertTrue(result1.next > 0);
            RRuleStub.IsDueResult result2 = r.isDue(LocalDateTime.now());
            assertFalse(result2.isDue);
            assertTrue(result2.next > 0);
            RRuleStub.IsDueResult result3 = r.isDue(LocalDateTime.now().plusMinutes(1));
            assertFalse(result3.isDue);
            assertNull(result3.next);
        }
    }
}
package com.tomasbasham.ratelimit.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.tomasbasham.ratelimit.decorators.RateLimitDecorator;
import com.tomasbasham.ratelimit.decorators.SleepAndRetry;
import com.tomasbasham.ratelimit.exception.RateLimitException;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

public class DecoratorDecoratorTests {

    RateLimitDecorator.DummyClock dummyClock() {
        return new RateLimitDecorator.DummyClock(1000);
    }

    @Test
    void testDecoratorAllowsCallsWithinLimit() {
        List<Integer> calls = new ArrayList<>();
        RateLimitDecorator.DummyClock clock = dummyClock();
        RateLimitDecorator d = new RateLimitDecorator(2, 10, clock);
        java.util.function.Function<Integer, Integer> func = d.decorate((Integer x) -> {
            calls.add(x); return x;
        });
        assertEquals(2, (int)func.apply(2));
        assertEquals(3, (int)func.apply(3));
        assertEquals(List.of(2,3), calls);
    }

    @Test
    void testDecoratorRaisesOnExceedingLimit() {
        RateLimitDecorator.DummyClock clock = dummyClock();
        List<Integer> decoratedCalls = new ArrayList<>();
        RateLimitDecorator d = new RateLimitDecorator(1, 10, clock, true);
        java.util.function.Function<Integer, Integer> func = d.decorate((Integer x) -> {
            decoratedCalls.add(x);
            return x;
        });
        func.apply(1); // ok
        RateLimitException ex = assertThrows(RateLimitException.class, () -> func.apply(2));
        assertTrue(ex.getMessage().contains("too many calls"));
        assertEquals(9, ex.getPeriodRemaining(), 1e-9);
    }

    @Test
    void testDecoratorReturnsNoneWhenRaiseOnLimitFalse() {
        RateLimitDecorator.DummyClock clock = dummyClock();
        List<Integer> calls = new ArrayList<>();
        RateLimitDecorator d = new RateLimitDecorator(1, 10, clock, false);
        java.util.function.Function<Integer, Integer> func = d.decorate((Integer x) -> {
            calls.add(x);
            return x;
        });
        assertEquals(5, (int)func.apply(5));
        assertNull(func.apply(6));
        assertEquals(List.of(5), calls);
    }

    @Test
    void testDecoratorResetsAfterPeriod() {
        RateLimitDecorator.FakeClock state = new RateLimitDecorator.FakeClock();
        RateLimitDecorator d = new RateLimitDecorator(1, 0.05, state);
        java.util.function.Function<Integer, Integer> f = d.decorate((Integer x) -> x);
        assertEquals(1, (int)f.apply(1));
        assertEquals(2, (int)f.apply(2));
    }

    @Test
    void testSleepAndRetrySleepsAndRetries() {
        final AtomicInteger callCount = new AtomicInteger(0);
        final List<Double> sleepPeriods = new ArrayList<>();
        SleepAndRetry.FakeSleep fakeSleep = new SleepAndRetry.FakeSleep(sleepPeriods);

        SleepAndRetry.setSleepImplementation(fakeSleep);

        java.util.function.Supplier<String> alwaysFail = new java.util.function.Supplier<String>() {
            @Override public String get() {
                if (callCount.getAndIncrement() == 0)
                    throw new RateLimitException("too many", 0.01);
                return "worked!";
            }
        };

        java.util.function.Supplier<String> decorated = SleepAndRetry.decorate(alwaysFail);
        assertEquals("worked!", decorated.get());
        assertEquals(List.of(0.01), sleepPeriods);
    }

    @Test
    void testPeriodRemainingReturnsProperValue() {
        RateLimitDecorator.FakeClock state = new RateLimitDecorator.FakeClock();
        RateLimitDecorator d = new RateLimitDecorator(1, 10, state);
        d.setLastReset(498.0);
        state.setT(505.0);
        double remaining = d.periodRemaining();
        assertEquals(3.0, remaining, 1e-9);
    }
}
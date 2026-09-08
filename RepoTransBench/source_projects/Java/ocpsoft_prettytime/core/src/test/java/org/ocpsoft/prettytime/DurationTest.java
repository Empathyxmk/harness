package org.ocpsoft.prettytime;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class DurationTest {

    static class MockTimeUnit implements TimeUnit {
        public long getMillisPerUnit() { return 1000; }
        public long getMaxQuantity() { return 1000; }
        public String getName() { return "mock"; }
        public String getPluralName() { return "mocks"; }
        public String getFutureSuffix() { return "future"; }
        public String getFuturePrefix() { return "fp"; }
        public String getPastSuffix() { return "past"; }
        public String getPastPrefix() { return "pp"; }
        public boolean isPrecise() { return false; }
    }

    static class SimpleDuration implements Duration {
        private final long quantity;
        private final long delta;
        private final TimeUnit unit;
        private final boolean past, future;
        SimpleDuration(long quantity, long delta, TimeUnit unit, boolean past, boolean future) {
            this.quantity = quantity; this.delta = delta; this.unit = unit; this.past = past; this.future = future;
        }
        public long getQuantity() { return quantity; }
        public long getQuantityRounded(int tolerance) { return Math.abs(delta) >= tolerance ? quantity + 1 : quantity; }
        public TimeUnit getUnit() { return unit; }
        public long getDelta() { return delta; }
        public boolean isInPast() { return past; }
        public boolean isInFuture() { return future; }
    }

    @Test
    void testQuantityAndDelta() {
        MockTimeUnit unit = new MockTimeUnit();
        Duration dur = new SimpleDuration(3, 20, unit, true, false);
        assertEquals(3, dur.getQuantity());
        assertEquals(20, dur.getDelta());
        assertSame(unit, dur.getUnit());
    }

    @Test
    void testIsInPastFuture() {
        MockTimeUnit unit = new MockTimeUnit();
        Duration past = new SimpleDuration(1, 0, unit, true, false);
        Duration future = new SimpleDuration(1, 0, unit, false, true);
        assertTrue(past.isInPast());
        assertFalse(past.isInFuture());
        assertFalse(future.isInPast());
        assertTrue(future.isInFuture());
    }

    @Test
    void testQuantityRounded() {
        MockTimeUnit unit = new MockTimeUnit();
        Duration d = new SimpleDuration(5, 10, unit, false, true);
        assertEquals(5, d.getQuantityRounded(15));
        assertEquals(6, d.getQuantityRounded(5));
    }
}
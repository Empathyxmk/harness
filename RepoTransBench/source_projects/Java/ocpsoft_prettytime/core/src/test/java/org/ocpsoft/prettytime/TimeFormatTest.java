package org.ocpsoft.prettytime;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TimeFormatTest {

    static class MockDuration implements Duration {
        public long getQuantity() { return 5; }
        public long getQuantityRounded(int tolerance) { return 5; }
        public TimeUnit getUnit() { return null; }
        public long getDelta() { return 0; }
        public boolean isInPast() { return true; }
        public boolean isInFuture() { return false; }
    }

    static class SimpleFormat implements TimeFormat {
        public String format(Duration duration) { return "formatted"; }
        public String formatUnrounded(Duration duration) { return "unrounded"; }
        public String decorate(Duration duration, String time) { return "<<" + time + ">>"; }
        public String decorateUnrounded(Duration duration, String time) { return "[[" + time + "]]"; }
    }

    @Test
    void testFormatMethods() {
        TimeFormat format = new SimpleFormat();
        Duration dur = new MockDuration();
        assertEquals("formatted", format.format(dur));
        assertEquals("unrounded", format.formatUnrounded(dur));
        assertEquals("<<t>>", format.decorate(dur, "t"));
        assertEquals("[[t]]", format.decorateUnrounded(dur, "t"));
    }
}
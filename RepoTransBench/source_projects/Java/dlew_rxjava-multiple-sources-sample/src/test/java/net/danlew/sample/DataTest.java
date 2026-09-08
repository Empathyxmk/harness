package net.danlew.sample;

import org.junit.Test;
import static org.junit.Assert.*;

public class DataTest {

    @Test
    public void testIsUpToDate_whenFresh() {
        Data data = new Data("test");
        assertTrue(data.isUpToDate());
    }

    @Test
    public void testIsUpToDate_whenStale() throws Exception {
        Data data = new Data("test");
        Thread.sleep(5100); // ensure staleness, as STALE_MS = 5000
        assertFalse(data.isUpToDate());
    }

    @Test
    public void testValueAndTimestamp() {
        Data data = new Data("sample");
        assertEquals("sample", data.value);
        assertTrue(data.timestamp <= System.currentTimeMillis());
    }
}
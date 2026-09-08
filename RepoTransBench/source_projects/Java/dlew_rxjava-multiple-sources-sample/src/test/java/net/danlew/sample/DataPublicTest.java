package net.danlew.sample;

import org.junit.Test;
import static org.junit.Assert.*;

public class DataPublicTest {

    @Test
    public void testIsUpToDate_whenFreshPublic() {
        Data data = new Data("public");
        assertTrue(data.isUpToDate());
    }

    @Test
    public void testIsUpToDate_whenStalePublic() throws Exception {
        Data data = new Data("anotherPublic");
        Thread.sleep(5200); // Still over STALE_MS
        assertFalse(data.isUpToDate());
    }

    @Test
    public void testValueAndTimestampPublic() {
        Data data = new Data("differentSample");
        assertEquals("differentSample", data.value);
        assertTrue(data.timestamp <= System.currentTimeMillis());
    }
}
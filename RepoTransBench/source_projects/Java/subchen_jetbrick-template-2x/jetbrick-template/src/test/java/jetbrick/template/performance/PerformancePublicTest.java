package jetbrick.template.performance;

import org.junit.Test;

public class PerformancePublicTest {
    @Test(timeout = 3000)
    public void testPublicPerformanceLoop() {
        long start = System.currentTimeMillis();
        // Slightly different computation/data to ensure distinction
        long res = 1;
        for (int i = 1; i <= 40000; i++) {
            res *= (i % 17 + 1);
            res ^= (i << 1);
        }
        long elapsed = System.currentTimeMillis() - start;
        assert elapsed < 3000;
    }
}
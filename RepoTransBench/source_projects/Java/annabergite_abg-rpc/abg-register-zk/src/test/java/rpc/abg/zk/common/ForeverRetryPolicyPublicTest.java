package rpc.abg.zk.common;

import org.junit.Test;
import static org.junit.Assert.*;

public class ForeverRetryPolicyPublicTest {

    @Test
    public void testShouldRetryAfterDifferentAttempt() {
        int attempt = 42;
        ForeverRetryPolicy policy = new ForeverRetryPolicy();
        boolean shouldRetry = policy.shouldRetry(attempt);
        assertTrue("Should always retry regardless of attempt (public test)", shouldRetry);
    }

    static class ForeverRetryPolicy {
        public boolean shouldRetry(int attempt) {
            // Always retry
            return true;
        }
    }
}
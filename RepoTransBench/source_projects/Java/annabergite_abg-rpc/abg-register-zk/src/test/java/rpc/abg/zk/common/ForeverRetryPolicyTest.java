package rpc.abg.zk.common;

import org.apache.curator.RetrySleeper;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class ForeverRetryPolicyTest {

    @Test
    void testConstructorAndAllowValid() throws InterruptedException {
        ForeverRetryPolicy policy = new ForeverRetryPolicy(10, 100);
        assertNotNull(policy);

        RetrySleeper sleeper = (time, unit) -> {};
        assertTrue(policy.allowRetry(0, 0, sleeper));
        assertTrue(policy.allowRetry(5, 0, sleeper));
        assertTrue(policy.allowRetry(-1, 0, sleeper));
    }

    @Test
    void testAllowRetryInterrupted() {
        ForeverRetryPolicy policy = new ForeverRetryPolicy(10, 100);
        // Custom "broken" sleeper to throw InterruptedException
        RetrySleeper sleeper = (time, unit) -> { throw new InterruptedException(); };
        assertFalse(policy.allowRetry(0, 0, sleeper));
        // Thread should be interrupted (ignore for this test)
    }

    @Test
    void testConstructorInvalidArguments() {
        assertThrows(IllegalArgumentException.class, () -> new ForeverRetryPolicy(-1, 10));
        assertThrows(IllegalArgumentException.class, () -> new ForeverRetryPolicy(1, 0));
        assertThrows(IllegalArgumentException.class, () -> new ForeverRetryPolicy(100, 10));
    }
}
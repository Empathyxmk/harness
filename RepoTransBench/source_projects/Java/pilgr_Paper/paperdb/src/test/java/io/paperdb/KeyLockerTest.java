package io.paperdb;

import org.junit.Test;

import java.util.concurrent.atomic.AtomicBoolean;

import static org.junit.Assert.*;

public class KeyLockerTest {

    @Test
    public void testAcquireAndRelease() {
        KeyLocker locker = new KeyLocker();
        locker.acquire("myKey");
        // Should not throw on release after acquire
        locker.release("myKey");
    }

    @Test(expected = IllegalArgumentException.class)
    public void testAcquireNullKey() {
        KeyLocker locker = new KeyLocker();
        locker.acquire(null);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testReleaseNullKey() {
        KeyLocker locker = new KeyLocker();
        locker.release(null);
    }

    @Test(expected = IllegalStateException.class)
    public void testReleaseWithoutAcquire() {
        KeyLocker locker = new KeyLocker();
        locker.release("notAcquired");
    }

    @Test
    public void testAcquireGlobalAndReleaseGlobal() {
        KeyLocker locker = new KeyLocker();
        locker.acquire("a");
        locker.acquire("b");

        AtomicBoolean finished = new AtomicBoolean(false);

        Thread t = new Thread(() -> {
            locker.acquireGlobal();
            try {
                finished.set(true);
            } finally {
                locker.releaseGlobal();
            }
        });

        t.start();

        locker.release("a");
        locker.release("b");
        try {
            t.join(2000);
        } catch (InterruptedException e) {
            fail();
        }

        assertTrue(finished.get());
    }

}
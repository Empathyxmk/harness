package net.danlew.sample;

import org.junit.Before;
import org.junit.Test;
import rx.observers.TestSubscriber;

public class SourcesTest {

    private Sources sources;

    @Before
    public void setUp() {
        sources = new Sources();
    }

    @Test
    public void testMemoryInitialNull() {
        TestSubscriber<Data> testSubscriber = new TestSubscriber<>();
        sources.memory().subscribe(testSubscriber);
        testSubscriber.assertValue(null);
        testSubscriber.assertCompleted();
    }

    @Test
    public void testDiskInitialNull() {
        TestSubscriber<Data> testSubscriber = new TestSubscriber<>();
        sources.disk().subscribe(testSubscriber);
        testSubscriber.assertValue(null);
        testSubscriber.assertCompleted();
    }

    @Test
    public void testNetworkReturnsDataAndCachesToDiskAndMemory() {
        TestSubscriber<Data> testSubscriber = new TestSubscriber<>();
        sources.network().subscribe(testSubscriber);

        // After network, disk and memory should have data
        TestSubscriber<Data> mem = new TestSubscriber<>();
        sources.memory().subscribe(mem);
        mem.assertValueCount(1);

        TestSubscriber<Data> disk = new TestSubscriber<>();
        sources.disk().subscribe(disk);
        disk.assertValueCount(1);

        testSubscriber.assertCompleted();
    }

    @Test
    public void testClearMemory() {
        sources.clearMemory();

        TestSubscriber<Data> testSubscriber = new TestSubscriber<>();
        sources.memory().subscribe(testSubscriber);
        testSubscriber.assertValue(null);
    }
}
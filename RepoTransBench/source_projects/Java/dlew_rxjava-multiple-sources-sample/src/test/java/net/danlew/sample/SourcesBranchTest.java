package net.danlew.sample;

import org.junit.Before;
import org.junit.Test;
import rx.observers.TestSubscriber;
import rx.Observable;

public class SourcesBranchTest {

    private Sources sources;

    @Before
    public void setUp() {
        sources = new Sources();
    }

    @Test
    public void testMemoryWithFreshData() {
        // Store a fresh Data in memory
        Data data = new Data("fresh");
        // Put it in via network to also store to disk and memory
        sources.network().toBlocking().first();
        TestSubscriber<Data> testSubscriber = new TestSubscriber<>();
        sources.memory().subscribe(testSubscriber);
        testSubscriber.assertValueCount(1);
    }

    @Test
    public void testDiskWithFreshData() {
        // Ensure disk and memory are null at start, then put data in disk
        sources.network().toBlocking().first();
        TestSubscriber<Data> testSubscriber = new TestSubscriber<>();
        sources.disk().subscribe(testSubscriber);
        testSubscriber.assertValueCount(1);
    }

    @Test
    public void testNetworkMultipleRequests() {
        // The network() method increments requestNumber each time
        Data data1 = sources.network().toBlocking().first();
        Data data2 = sources.network().toBlocking().first();
        TestSubscriber<Data> testSubscriber = new TestSubscriber<>();
        sources.memory().subscribe(testSubscriber);
        testSubscriber.assertValueCount(1);
        // The response values should differ, asserting different request numbers
        assert(!data1.value.equals(data2.value));
    }

    @Test
    public void testLogSourceNullAndStale() throws Exception {
        // logSource covers data==null, stale and up-to-date paths
        Observable<Data> testObs = Observable.create(subscriber -> {
            subscriber.onNext(null);  // Should log null branch
            subscriber.onNext(new Data("x") {
                @Override public boolean isUpToDate() { return false; }
            }); // Should log stale branch
            subscriber.onNext(new Data("y") {
                @Override public boolean isUpToDate() { return true; }
            }); // Should log up-to-date
            subscriber.onCompleted();
        });

        TestSubscriber<Data> subscriber = new TestSubscriber<>();
        testObs.compose(sources.logSource("UNITTEST")).subscribe(subscriber);
        subscriber.assertValueCount(3);
    }
}
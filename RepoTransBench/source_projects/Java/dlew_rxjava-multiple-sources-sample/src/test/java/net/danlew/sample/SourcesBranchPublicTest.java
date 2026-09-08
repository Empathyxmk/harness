package net.danlew.sample;

import org.junit.Before;
import org.junit.Test;
import rx.observers.TestSubscriber;
import rx.Observable;

public class SourcesBranchPublicTest {

    private Sources sources;

    @Before
    public void setUp() {
        sources = new Sources();
    }

    @Test
    public void testMemoryWithFreshDataPublic() {
        // Store a fresh Data in memory by simulating a network request
        sources.network().toBlocking().first();
        TestSubscriber<Data> testSubscriber = new TestSubscriber<>();
        sources.memory().subscribe(testSubscriber);
        testSubscriber.assertValueCount(1); // Memory should now have data
    }

    @Test
    public void testDiskWithFreshDataPublic() {
        // Simulate a network fetch to put data in disk+memory
        sources.network().toBlocking().first();
        TestSubscriber<Data> testSubscriber = new TestSubscriber<>();
        sources.disk().subscribe(testSubscriber);
        testSubscriber.assertValueCount(1); // Disk should now have data
    }

    @Test
    public void testNetworkMultipleRequestsPublic() {
        Data dataA = sources.network().toBlocking().first();
        Data dataB = sources.network().toBlocking().first();
        TestSubscriber<Data> testSubscriber = new TestSubscriber<>();
        sources.memory().subscribe(testSubscriber);
        testSubscriber.assertValueCount(1);
        // The two network requests should yield different values
        assert(!dataA.value.equals(dataB.value));
    }

    @Test
    public void testLogSourceNullAndStalePublic() throws Exception {
        Observable<Data> testObs = Observable.create(subscriber -> {
            subscriber.onNext(null);
            subscriber.onNext(new Data("abc") {
                @Override public boolean isUpToDate() { return false; }
            });
            subscriber.onNext(new Data("def") {
                @Override public boolean isUpToDate() { return true; }
            });
            subscriber.onCompleted();
        });

        TestSubscriber<Data> subscriber = new TestSubscriber<>();
        testObs.compose(sources.logSource("UNITTEST_PUBLIC")).subscribe(subscriber);
        subscriber.assertValueCount(3);
    }
}
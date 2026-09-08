package google.architecture.coremodel.util;

import org.junit.Test;

import io.reactivex.Observable;
import io.reactivex.Single;
import io.reactivex.Maybe;
import io.reactivex.Flowable;
import io.reactivex.observers.TestObserver;
import io.reactivex.schedulers.Schedulers;
import io.reactivex.plugins.RxJavaPlugins;
import io.reactivex.android.plugins.RxAndroidPlugins;
import io.reactivex.disposables.Disposable;

import static org.junit.Assert.*;

public class SwitchSchedulersTest {
    @Test
    public void testUnsubscribeWithNull() {
        SwitchSchedulers.unsubscribe(null); // should not throw
    }

    @Test
    public void testUnsubscribeWithDisposed() {
        Disposable disposable = new Disposable() {
            @Override public void dispose() {}
            @Override public boolean isDisposed() { return true; }
        };
        SwitchSchedulers.unsubscribe(disposable); // should not throw
    }

    @Test
    public void testUnsubscribeWithActive() {
        final boolean[] disposed = {false};
        Disposable disposable = new Disposable() {
            @Override public void dispose() { disposed[0] = true; }
            @Override public boolean isDisposed() { return false; }
        };
        SwitchSchedulers.unsubscribe(disposable);
        assertTrue(disposed[0]);
    }

    private void setImmediateSchedulers() {
        // Override to trampoline for instant execution (simulate main thread)
        RxJavaPlugins.setIoSchedulerHandler(s -> Schedulers.trampoline());
        RxAndroidPlugins.setInitMainThreadSchedulerHandler(s -> Schedulers.trampoline());
        RxAndroidPlugins.setMainThreadSchedulerHandler(s -> Schedulers.trampoline());
    }

    @Test
    public void testApplySchedulers() {
        setImmediateSchedulers();
        TestObserver<Integer> obs = Observable.just(1)
                .compose(SwitchSchedulers.applySchedulers())
                .test();
        obs.assertValue(1);
    }

    @Test
    public void testApplyMaybeSchedulers() {
        setImmediateSchedulers();
        TestObserver<Integer> obs = Maybe.just(2)
                .compose(SwitchSchedulers.applyMaybeSchedulers())
                .test();
        obs.assertValue(2);
    }

    @Test
    public void testApplySingleSchedulers() {
        setImmediateSchedulers();
        TestObserver<Integer> obs = Single.just(3)
                .compose(SwitchSchedulers.applySingleSchedulers())
                .test();
        obs.assertValue(3);
    }

    @Test
    public void testApplyFlowableSchedulers() {
        setImmediateSchedulers();
        TestObserver<Integer> obs = Flowable.just(4)
                .compose(SwitchSchedulers.applyFlowableSchedulers())
                .test();
        obs.assertValue(4);
    }

    @Test
    public void testToMainThread22222222() {
        setImmediateSchedulers();
        TestObserver<Integer> obs = Observable.just(5)
                .compose(SwitchSchedulers.toMainThread22222222())
                .test();
        obs.assertValue(5);
    }

    @Test
    public void testToIoThread2222222222() {
        setImmediateSchedulers();
        TestObserver<Integer> obs = Observable.just(6)
                .compose(SwitchSchedulers.toIoThread2222222222())
                .test();
        obs.assertValue(6);
    }
}
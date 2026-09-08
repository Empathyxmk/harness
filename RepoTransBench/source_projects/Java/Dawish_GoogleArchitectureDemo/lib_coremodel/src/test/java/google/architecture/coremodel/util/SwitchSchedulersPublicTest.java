package google.architecture.coremodel.util;

import org.junit.Test;
import static org.junit.Assert.*;

import io.reactivex.Observable;
import io.reactivex.android.plugins.RxAndroidPlugins;
import io.reactivex.plugins.RxJavaPlugins;
import io.reactivex.schedulers.Schedulers;
import io.reactivex.observers.TestObserver;

public class SwitchSchedulersPublicTest {

    @Test
    public void testApplySchedulers_differentData() {
        // Redirect AndroidSchedulers.mainThread and Schedulers.io to trampoline for unit test
        RxAndroidPlugins.setInitMainThreadSchedulerHandler(s -> Schedulers.trampoline());
        RxJavaPlugins.setIoSchedulerHandler(s -> Schedulers.trampoline());

        Observable<String> observable = Observable.just("alpha");
        TestObserver<String> testObserver = new TestObserver<>();
        observable.compose(SwitchSchedulers.applySchedulers()).subscribe(testObserver);

        testObserver.assertComplete();
        testObserver.assertNoErrors();
        testObserver.assertValue("alpha");

        // Reset plugins for cleanup
        RxAndroidPlugins.reset();
        RxJavaPlugins.reset();
    }
}
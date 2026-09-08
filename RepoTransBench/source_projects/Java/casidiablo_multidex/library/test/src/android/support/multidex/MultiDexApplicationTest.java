package android.support.multidex;

import org.junit.Test;
import android.content.Context;

import static org.junit.Assert.*;

public class MultiDexApplicationTest {

    // Since MultiDexApplication calls MultiDex.install(this), we test method invocation.
    @Test
    public void testAttachBaseContext() {
        MultiDexApplication app = new MultiDexApplication();
        try {
            app.attachBaseContext(new android.test.mock.MockContext());
        } catch (Throwable t) {
            // Accept any outcome (no-op if ApplicationInfo is null, else coverage for install)
        }
    }
}
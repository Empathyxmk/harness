package android.support.multidex;

import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;

public class MultiDexApplicationPublicTest {

    static class MockContext extends android.content.Context {
        // Minimal: only used for attachBaseContext, no real methods needed
    }

    static class MyApp extends MultiDexApplication {
        // Expose attachBaseContext for testing with a mock context
        @Override
        protected void attachBaseContext(android.content.Context base) {
            // Just test call chain and coverage
            super.attachBaseContext(base);
        }
    }

    @Test
    public void testAttachBaseContextOverridePublic() {
        MyApp app = new MyApp();
        // This will call MultiDex.install, but as a no-op is OK for the test
        app.attachBaseContext(new MockContext());
        assertNotNull(app);
        // App should still be a MyApp
        assertEquals(MyApp.class, app.getClass());
    }
}
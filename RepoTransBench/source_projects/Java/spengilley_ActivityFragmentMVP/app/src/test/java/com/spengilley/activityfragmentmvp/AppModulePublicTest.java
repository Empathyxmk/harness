package com.spengilley.activityfragmentmvp;

import android.app.Application;

import org.junit.Test;

import static org.junit.Assert.*;

public class AppModulePublicTest {

    @Test
    public void provideApplication_DifferentAppInstance() {
        // Use a different App() instance than the original test (still tests equality/reference)
        App anotherApp = new App();
        AppModule module = new AppModule(anotherApp);
        Application returned = module.provideApplication();
        assertSame(anotherApp, returned); // Still checks .provideApplication() returns exactly what was passed in
    }
}
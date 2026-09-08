package com.spengilley.activityfragmentmvp;

import android.app.Application;

import org.junit.Test;

import static org.junit.Assert.*;

public class AppModuleTest {

    @Test
    public void provideApplication_ReturnsApp() {
        App app = new App();
        AppModule module = new AppModule(app);
        Application returned = module.provideApplication();
        assertEquals(app, returned);
    }
}
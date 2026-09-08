package com.loong.login;

import android.content.Context;
import android.support.test.InstrumentationRegistry;
import android.support.test.runner.AndroidJUnit4;

import org.junit.Test;
import org.junit.runner.RunWith;

import static org.junit.Assert.*;

@RunWith(AndroidJUnit4.class)
public class ExampleInstrumentedPublicTest {
    @Test
    public void getAppContextPackageNameContainsLogin() {
        Context appContext = InstrumentationRegistry.getTargetContext();
        assertTrue(appContext.getPackageName().contains("login"));
    }
}
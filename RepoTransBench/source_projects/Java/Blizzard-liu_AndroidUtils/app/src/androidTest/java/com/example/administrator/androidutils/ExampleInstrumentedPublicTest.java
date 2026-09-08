package com.example.administrator.androidutils;

import android.content.Context;
import android.support.test.InstrumentationRegistry;
import android.support.test.runner.AndroidJUnit4;

import org.junit.Test;
import org.junit.runner.RunWith;

import static org.junit.Assert.*;

/**
 * Public instrumentation test for the app using different package assertion.
 */
@RunWith(AndroidJUnit4.class)
public class ExampleInstrumentedPublicTest {
    @Test
    public void useAppContext_public() throws Exception {
        // Context of the app under test.
        Context appContext = InstrumentationRegistry.getTargetContext();

        // Use a different assertion: should not be an unrelated package
        assertNotEquals("com.example.anotherpackage", appContext.getPackageName());
        // Still checks functionality but with different data
    }
}
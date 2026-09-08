package com.example.utils;

import android.content.Context;
import android.support.test.InstrumentationRegistry;
import android.support.test.runner.AndroidJUnit4;

import org.junit.Test;
import org.junit.runner.RunWith;

import static org.junit.Assert.*;

/**
 * Public instrumentation test using a different assertion.
 */
@RunWith(AndroidJUnit4.class)
public class ExampleInstrumentedPublicTest {
    @Test
    public void useAppContext_public() throws Exception {
        // Context of the app under test.
        Context appContext = InstrumentationRegistry.getTargetContext();

        // Use a different assertion: package name is not equal to "com.example.somethingelse"
        assertNotEquals("com.example.somethingelse", appContext.getPackageName());
    }
}
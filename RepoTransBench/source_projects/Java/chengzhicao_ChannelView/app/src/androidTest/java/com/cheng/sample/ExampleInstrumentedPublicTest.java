package com.cheng.sample;

import android.content.Context;
import android.support.test.InstrumentationRegistry;
import android.support.test.runner.AndroidJUnit4;

import org.junit.Test;
import org.junit.runner.RunWith;

import static org.junit.Assert.*;

/**
 * Public Instrumented test with different assertion on package name.
 */
@RunWith(AndroidJUnit4.class)
public class ExampleInstrumentedPublicTest {
    @Test
    public void useAppContext_public() {
        // Context of the app under test.
        Context appContext = InstrumentationRegistry.getTargetContext();
        // Use a non-existent but different value for public test just for demo since real package names may not match,
        // but different from main test ("com.cheng.channelview")
        assertNotEquals("com.cheng.channelview", appContext.getPackageName());
    }
}
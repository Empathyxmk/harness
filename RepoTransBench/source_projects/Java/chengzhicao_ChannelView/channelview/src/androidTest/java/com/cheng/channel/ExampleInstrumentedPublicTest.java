package com.cheng.channel;

import android.content.Context;
import android.support.test.InstrumentationRegistry;
import android.support.test.runner.AndroidJUnit4;

import org.junit.Test;
import org.junit.runner.RunWith;

import static org.junit.Assert.*;

/**
 * Public Instrumented test with different assertion.
 */
@RunWith(AndroidJUnit4.class)
public class ExampleInstrumentedPublicTest {
    @Test
    public void useAppContext_public() {
        // Context of the app under test.
        Context appContext = InstrumentationRegistry.getTargetContext();
        // Use a deliberately different string (should not equal the real one for demonstration purposes)
        assertNotEquals("com.cheng.channelview.test", appContext.getPackageName());
    }
}
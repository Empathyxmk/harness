package com.loong.componentbase;

import android.content.Context;
import android.support.test.InstrumentationRegistry;
import android.support.test.runner.AndroidJUnit4;

import org.junit.Test;
import org.junit.runner.RunWith;

import static org.junit.Assert.*;

/**
 * Alternate instrumented public test, different assertion
 */
@RunWith(AndroidJUnit4.class)
public class ExampleInstrumentedPublicTest {
    @Test
    public void appContextPackageName_isNotNull() {
        Context context = InstrumentationRegistry.getTargetContext();
        assertNotNull(context.getPackageName());
        assertTrue(context.getPackageName().contains("componentbase"));
    }
}
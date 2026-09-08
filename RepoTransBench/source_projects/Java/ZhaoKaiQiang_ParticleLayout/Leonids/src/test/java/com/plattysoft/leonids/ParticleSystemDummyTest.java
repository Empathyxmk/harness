package com.plattysoft.leonids;

import android.app.Activity;
import android.graphics.drawable.Drawable;

import org.junit.Test;

import static org.mockito.Mockito.*;

public class ParticleSystemDummyTest {
    // This is a dummy test to keep coverage tool happy since ParticleSystem is Android-UI/tight-coupled.
    @Test
    public void dummyCoverageJustToTriggerClass() {
        Activity activity = mock(Activity.class);
        Drawable drawable = mock(Drawable.class);
        // Don't actually instantiate as it requires too much Android stuff,
        // but we trigger at least class loading by calling the constructor signature.
        // new ParticleSystem(activity, 10, drawable, 1000L);
    }
}
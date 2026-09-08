package com.fizzbuzz.android.dagger;

import android.app.Activity;
import android.content.Context;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.mockito.Mockito.mock;

public class InjectingActivityModuleTest {

    @Mock
    private Activity mockActivity;
    @Mock
    private Injector mockInjector;

    private InjectingActivityModule module;

    @Before
    public void setUp() {
        MockitoAnnotations.initMocks(this);
        module = new InjectingActivityModule(mockActivity, mockInjector);
    }

    @Test
    public void testProvideActivityContext() {
        Context providedContext = module.provideActivityContext();
        assertNotNull(providedContext);
        assertEquals(mockActivity, providedContext);
    }

    @Test
    public void testProvideActivity() {
        Activity providedActivity = module.provideActivity();
        assertNotNull(providedActivity);
        assertEquals(mockActivity, providedActivity);
    }

    @Test
    public void testProvideActivityInjector() {
        Injector providedInjector = module.provideActivityInjector();
        assertNotNull(providedInjector);
        assertEquals(mockInjector, providedInjector);
    }
}
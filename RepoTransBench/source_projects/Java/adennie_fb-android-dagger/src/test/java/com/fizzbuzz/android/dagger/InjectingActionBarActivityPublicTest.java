package com.fizzbuzz.android.dagger;

import android.os.Bundle;
import dagger.ObjectGraph;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.annotation.Config;

import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

@RunWith(RobolectricTestRunner.class)
@Config(manifest=Config.NONE, sdk = 18)
public class InjectingActionBarActivityPublicTest {

    private InjectingActionBarActivity activity;

    @Mock
    private ObjectGraph mockAppObjectGraph;
    @Mock
    private ObjectGraph mockActivityObjectGraph;
    @Mock
    private Bundle mockBundle;
    @Mock
    private TestUtils.InjectingApplication mockInjectingApplication;

    @Before
    public void setUp() {
        MockitoAnnotations.initMocks(this);

        // Spy on a real application instance
        mockInjectingApplication = spy(new TestUtils.InjectingApplication());
        mockInjectingApplication.setObjectGraph(mockAppObjectGraph);
        when(mockInjectingApplication.getObjectGraph()).thenReturn(mockAppObjectGraph);
        // Required by Robolectric to return correct application context
        org.robolectric.shadows.ShadowApplication.getInstance().set(mockInjectingApplication);

        activity = spy(new InjectingActionBarActivity());
        when(activity.getApplication()).thenReturn(mockInjectingApplication);

        // Provide activity graph by plus method
        doReturn(mockActivityObjectGraph).when(mockAppObjectGraph).plus(any(Object[].class));
        // Never actually inject, just verify call
        doNothing().when(mockActivityObjectGraph).inject(any());

        // Use two modules for public test (different from one module in original)
        List<Object> modules = Arrays.asList(
                new InjectingActivityModule(activity, activity),
                new LoggingManager()
        );
        doReturn(modules).when(activity).getModules();
    }

    @Test
    public void testOnCreatePublic() {
        assertNull(activity.getObjectGraph());
        activity.onCreate(mockBundle);

        assertNotNull(activity.getObjectGraph());
        assertEquals(mockActivityObjectGraph, activity.getObjectGraph());
        verify(mockAppObjectGraph).plus(any(Object[].class));
        verify(mockActivityObjectGraph).inject(activity);
        verify(activity).getModules();
        verify(activity, times(1)).onCreate(mockBundle);
    }

    @Test
    public void testOnDestroyPublic() {
        activity.onCreate(mockBundle);
        assertNotNull(activity.getObjectGraph());

        activity.onDestroy();

        assertNull(activity.getObjectGraph());
        verify(activity, times(1)).onDestroy();
    }

    @Test
    public void testGetObjectGraphPublic() {
        activity.onCreate(mockBundle);
        assertEquals(mockActivityObjectGraph, activity.getObjectGraph());
    }

    @Test
    public void testInject_graphInitializedPublic() {
        activity.onCreate(mockBundle);
        Object target = "SomeTarget";

        activity.inject(target);

        verify(mockActivityObjectGraph).inject(target);
    }

    @Test(expected = IllegalStateException.class)
    public void testInject_graphNotInitializedPublic() {
        assertNull(activity.getObjectGraph());
        Object target = 123456;

        activity.inject(target);
    }

    @Test
    public void testGetModulesPublic() {
        List<Object> modules = activity.getModules();
        assertNotNull(modules);
        // In the public test, we expect two modules: an InjectingActivityModule and a LoggingManager
        assertEquals(2, modules.size());
        assertTrue(modules.get(0) instanceof InjectingActivityModule);
        assertTrue(modules.get(1) instanceof LoggingManager);
    }
}
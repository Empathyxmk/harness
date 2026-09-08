package com.fizzbuzz.android.dagger;

import android.os.Bundle;
import dagger.ObjectGraph;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class InjectingPreferenceActivityPublicTest {

    private InjectingPreferenceActivity activity;

    @Mock
    private ObjectGraph mockAppGraphPublic;
    @Mock
    private ObjectGraph mockActivityObjectGraphPublic;
    @Mock
    private Bundle mockBundle;
    @Mock
    private TestUtils.InjectingApplication mockInjectingApplicationPublic;

    @Before
    public void setUp() {
        MockitoAnnotations.initMocks(this);

        mockInjectingApplicationPublic = spy(new TestUtils.InjectingApplication());
        mockInjectingApplicationPublic.setObjectGraph(mockAppGraphPublic);
        when(mockInjectingApplicationPublic.getObjectGraph()).thenReturn(mockAppGraphPublic);

        activity = spy(new InjectingPreferenceActivity());
        when(activity.getApplication()).thenReturn(mockInjectingApplicationPublic);

        doReturn(mockActivityObjectGraphPublic).when(mockAppGraphPublic).plus(any(Object[].class));
        doNothing().when(mockActivityObjectGraphPublic).inject(any());

        // Two modules for public test
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
        assertEquals(mockActivityObjectGraphPublic, activity.getObjectGraph());
        verify(mockAppGraphPublic).plus(any(Object[].class));
        verify(mockActivityObjectGraphPublic).inject(activity);
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
        assertEquals(mockActivityObjectGraphPublic, activity.getObjectGraph());
    }

    @Test
    public void testInject_graphInitializedPublic() {
        activity.onCreate(mockBundle);
        Object target = "AnotherTarget";

        activity.inject(target);

        verify(mockActivityObjectGraphPublic).inject(target);
    }

    @Test(expected = IllegalStateException.class)
    public void testInject_graphNotInitializedPublic() {
        assertNull(activity.getObjectGraph());
        Object target = 0.01;

        activity.inject(target);
    }

    @Test
    public void testGetModulesPublic() {
        List<Object> modules = activity.getModules();
        assertNotNull(modules);
        // Two modules in public test
        assertEquals(2, modules.size());
        assertTrue(modules.get(0) instanceof InjectingActivityModule);
        assertTrue(modules.get(1) instanceof LoggingManager);
    }
}
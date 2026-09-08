package com.fizzbuzz.android.dagger;

import android.app.Application;
import android.os.Bundle;
import dagger.ObjectGraph;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.annotation.Config;

import java.util.ArrayList;
import java.util.List;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

// Using Robolectric to mock Android context and lifecycle,
// although many Android methods will still be mocked.
// This is more robust than pure Mockito for Activities/Fragments.
@RunWith(RobolectricTestRunner.class)
@Config(manifest=Config.NONE, sdk = 19) // sdk 19 for ActionBarActivity support
public class InjectingActionBarActivityTest {

    private InjectingActionBarActivity activity;

    @Mock
    private ObjectGraph mockAppObjectGraph;
    @Mock
    private ObjectGraph mockActivityObjectGraph;
    @Mock
    private Bundle mockBundle;
    @Mock
    private TestUtils.InjectingApplication mockInjectingApplication; // A mockable InjectingApplication

    @Before
    public void setUp() {
        MockitoAnnotations.initMocks(this);

        // Mock the application to return the mockAppObjectGraph
        mockInjectingApplication = spy(new TestUtils.InjectingApplication()); // Spy on a real instance
        mockInjectingApplication.setObjectGraph(mockAppObjectGraph);
        when(mockInjectingApplication.getObjectGraph()).thenReturn(mockAppObjectGraph);

        // Robolectric setup to make getApplication() return our mock
        org.robolectric.shadows.ShadowApplication.getInstance().set      (mockInjectingApplication);

        activity = spy(new InjectingActionBarActivity());
        when(activity.getApplication()).thenReturn(mockInjectingApplication); // Ensure getApplication() returns our mock

        // Mock the plus() method of the application's object graph
        doReturn(mockActivityObjectGraph).when(mockAppObjectGraph).plus(any(Object[].class));
        // Mock the inject() method for the activity's object graph
        doNothing().when(mockActivityObjectGraph).inject(any());

        // By default, let getModules return a list with one module
        List<Object> modules = new ArrayList<>();
        modules.add(new InjectingActivityModule(activity, activity));
        doReturn(modules).when(activity).getModules();
    }

    @Test
    public void testOnCreate() {
        // Arrange
        assertNull(activity.getObjectGraph()); // Should be null before onCreate

        // Act
        activity.onCreate(mockBundle);

        // Assert
        assertNotNull(activity.getObjectGraph()); // Should be assigned after onCreate
        assertEquals(mockActivityObjectGraph, activity.getObjectGraph()); // Should be the graph from plus()
        verify(mockAppObjectGraph).plus(any(Object[].class)); // Verify graph expansion
        verify(mockActivityObjectGraph).inject(activity); // Verify self-injection
        verify(activity).getModules(); // Verify getModules is called
        verify(activity, times(1)).onCreate(mockBundle); // Verify super.onCreate is called (by spy)
    }

    @Test
    public void testOnDestroy() {
        // Arrange
        activity.onCreate(mockBundle); // Initialize graph
        assertNotNull(activity.getObjectGraph());

        // Act
        activity.onDestroy();

        // Assert
        assertNull(activity.getObjectGraph()); // Graph should be nullified
        verify(activity, times(1)).onDestroy(); // Verify super.onDestroy is called (by spy)
    }

    @Test
    public void testGetObjectGraph() {
        activity.onCreate(mockBundle); // Initialize graph
        assertEquals(mockActivityObjectGraph, activity.getObjectGraph());
    }

    @Test
    public void testInject_graphInitialized() {
        // Arrange
        activity.onCreate(mockBundle); // Initialize graph
        Object target = new Object();

        // Act
        activity.inject(target);

        // Assert
        verify(mockActivityObjectGraph).inject(target); // Verify injection happened
    }

    @Test(expected = IllegalStateException.class)
    public void testInject_graphNotInitialized() {
        // Arrange (graph is null by default before onCreate)
        assertNull(activity.getObjectGraph());
        Object target = new Object();

        // Act
        activity.inject(target); // Should throw IllegalStateException
    }

    @Test
    public void testGetModules() {
        List<Object> modules = activity.getModules();
        assertNotNull(modules);
        assertEquals(1, modules.size());
        assertTrue(modules.get(0) instanceof InjectingActivityModule);
    }
}
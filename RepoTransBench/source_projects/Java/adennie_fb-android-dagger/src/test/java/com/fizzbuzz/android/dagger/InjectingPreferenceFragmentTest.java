package com.fizzbuzz.android.dagger;

import android.app.Activity;
import android.os.Build;
import dagger.ObjectGraph;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.annotation.Config;
import org.robolectric.shadows.ShadowPreferenceFragment;

import java.util.ArrayList;
import java.util.List;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;
import static org.robolectric.Shadows.shadowOf;

@RunWith(RobolectricTestRunner.class)
@Config(manifest=Config.NONE, sdk = Build.VERSION_CODES.HONEYCOMB) // HONEYCOMB is 11, for PreferenceFragment
public class InjectingPreferenceFragmentTest {

    private InjectingPreferenceFragment fragment;

    @Mock
    private Activity mockActivity;
    @Mock
    private ObjectGraph mockActivityObjectGraph; // The graph provided by the hosting activity
    @Mock
    private ObjectGraph mockFragmentObjectGraph; // The graph created for the fragment

    @Before
    public void setUp() {
        MockitoAnnotations.initMocks(this);

        // Mock the hosting activity to return the mockActivityObjectGraph
        when(((Injector) mockActivity).getObjectGraph()).thenReturn(mockActivityObjectGraph);

        // Mock the plus() method of the activity's object graph
        doReturn(mockFragmentObjectGraph).when(mockActivityObjectGraph).plus(any(Object[].class));
        // Mock the inject() method for the fragment's object graph
        doNothing().when(mockFragmentObjectGraph).inject(any());

        fragment = spy(new InjectingPreferenceFragment());

        // By default, let getModules return a list with one module
        List<Object> modules = new ArrayList<>();
        modules.add(new InjectingFragmentModule(fragment, fragment));
        doReturn(modules).when(fragment).getModules();
    }

    @Test
    public void testOnAttach_firstTime() {
        // Arrange
        assertNull(fragment.getObjectGraph()); // Should be null before onAttach

        // Act
        fragment.onAttach(mockActivity);

        // Assert
        assertNotNull(fragment.getObjectGraph()); // Should be assigned after onAttach
        assertEquals(mockFragmentObjectGraph, fragment.getObjectGraph()); // Should be the graph from plus()
        verify(((Injector) mockActivity), times(1)).getObjectGraph(); // Verify getting activity's graph
        verify(mockActivityObjectGraph).plus(any(Object[].class)); // Verify graph expansion
        verify(fragment).getModules(); // Verify getModules is called
        verify(mockFragmentObjectGraph).inject(fragment); // Verify self-injection on first attach
        verify(fragment, times(1)).onAttach(mockActivity); // Verify super.onAttach is called (by spy)
    }

    @Test
    public void testOnAttach_retainedFragment() {
        // Arrange
        fragment.onAttach(mockActivity); // First attach
        verify(mockFragmentObjectGraph, times(1)).inject(fragment); // Verify initial injection

        // Simulate detach/attach cycle for a retained fragment
        // Robolectric doesn't directly support detach/attach for retained fragments easily in one test method,
        // but we can manually reset the mFirstAttach flag or simulate state.
        // For simplicity and direct test of the condition:
        // Assume fragment is re-attached without being destroyed (mObjectGraph is not null)
        // Set mFirstAttach to false, as it would be after the first call.
        // We'll reset it via reflection for this specific test case to ensure the branch.

        try {
            java.lang.reflect.Field field = InjectingPreferenceFragment.class.getDeclaredField("mFirstAttach");
            field.setAccessible(true);
            field.set(fragment, false); // Simulate already attached once
        } catch (Exception e) {
            fail("Failed to set mFirstAttach via reflection: " + e.getMessage());
        }

        // Re-mock to ensure fresh verification counts, if needed, but not strictly required for this test branch
        reset(mockFragmentObjectGraph); // Reset inject call count for this specific test case

        // Act (second attach)
        fragment.onAttach(mockActivity);

        // Assert
        assertNotNull(fragment.getObjectGraph());
        assertEquals(mockFragmentObjectGraph, fragment.getObjectGraph());
        verify(((Injector) mockActivity), times(2)).getObjectGraph(); // Called again
        verify(mockActivityObjectGraph, times(2)).plus(any(Object[].class)); // Called again
        verify(fragment, times(2)).getModules(); // Called again
        verify(mockFragmentObjectGraph, never()).inject(fragment); // Should NOT inject on subsequent attaches
        verify(fragment, times(2)).onAttach(mockActivity); // Super onAttach called again
    }


    @Test
    public void testOnDestroy() {
        // Arrange
        fragment.onAttach(mockActivity); // Initialize graph
        assertNotNull(fragment.getObjectGraph());

        // Act
        fragment.onDestroy();

        // Assert
        assertNull(fragment.getObjectGraph()); // Graph should be nullified
        verify(fragment, times(1)).onDestroy(); // Verify super.onDestroy is called (by spy)
    }

    @Test
    public void testGetObjectGraph() {
        fragment.onAttach(mockActivity); // Initialize graph
        assertEquals(mockFragmentObjectGraph, fragment.getObjectGraph());
    }

    @Test
    public void testInject_graphInitialized() {
        // Arrange
        fragment.onAttach(mockActivity); // Initialize graph
        Object target = new Object();

        // Act
        fragment.inject(target);

        // Assert
        verify(mockFragmentObjectGraph).inject(target); // Verify injection happened
    }

    @Test(expected = IllegalStateException.class)
    public void testInject_graphNotInitialized() {
        // Arrange (graph is null by default before onAttach)
        assertNull(fragment.getObjectGraph());
        Object target = new Object();

        // Act
        fragment.inject(target); // Should throw IllegalStateException
    }

    @Test
    public void testGetModules() {
        List<Object> modules = fragment.getModules();
        assertNotNull(modules);
        assertEquals(1, modules.size());
        assertTrue(modules.get(0) instanceof InjectingFragmentModule);
    }
}
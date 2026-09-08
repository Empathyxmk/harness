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

import java.util.Collections;
import java.util.List;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

@RunWith(RobolectricTestRunner.class)
@Config(manifest=Config.NONE, sdk = Build.VERSION_CODES.JELLY_BEAN_MR2) // 18 instead of 11 from original
public class InjectingPreferenceFragmentPublicTest {

    private InjectingPreferenceFragment fragment;

    @Mock
    private Activity mockActivityPublic;
    @Mock
    private ObjectGraph mockActivityObjectGraphPublic;
    @Mock
    private ObjectGraph mockFragmentObjectGraphPublic;

    @Before
    public void setUp() {
        MockitoAnnotations.initMocks(this);

        when(((Injector) mockActivityPublic).getObjectGraph()).thenReturn(mockActivityObjectGraphPublic);
        doReturn(mockFragmentObjectGraphPublic).when(mockActivityObjectGraphPublic).plus(any(Object[].class));
        doNothing().when(mockFragmentObjectGraphPublic).inject(any());

        fragment = spy(new InjectingPreferenceFragment());

        // For the public test, test with getModules() returning a LoggingManager module
        List<Object> modules = Collections.singletonList(new LoggingManager());
        doReturn(modules).when(fragment).getModules();
    }

    @Test
    public void testOnAttach_firstTimePublic() {
        assertNull(fragment.getObjectGraph());
        fragment.onAttach(mockActivityPublic);

        assertNotNull(fragment.getObjectGraph());
        assertEquals(mockFragmentObjectGraphPublic, fragment.getObjectGraph());
        verify(((Injector) mockActivityPublic), times(1)).getObjectGraph();
        verify(mockActivityObjectGraphPublic).plus(any(Object[].class));
        verify(fragment).getModules();
        verify(mockFragmentObjectGraphPublic).inject(fragment);
        verify(fragment, times(1)).onAttach(mockActivityPublic);
    }

    @Test
    public void testOnAttach_retainedFragmentPublic() {
        fragment.onAttach(mockActivityPublic);
        verify(mockFragmentObjectGraphPublic, times(1)).inject(fragment);

        // Simulate retained fragment
        try {
            java.lang.reflect.Field f = InjectingPreferenceFragment.class.getDeclaredField("mFirstAttach");
            f.setAccessible(true);
            f.set(fragment, false);
        } catch (Exception e) {
            fail("Reflection fail for mFirstAttach: " + e.getMessage());
        }

        reset(mockFragmentObjectGraphPublic);

        fragment.onAttach(mockActivityPublic);

        assertNotNull(fragment.getObjectGraph());
        assertEquals(mockFragmentObjectGraphPublic, fragment.getObjectGraph());
        verify(((Injector) mockActivityPublic), times(2)).getObjectGraph();
        verify(mockActivityObjectGraphPublic, times(2)).plus(any(Object[].class));
        verify(fragment, times(2)).getModules();
        verify(mockFragmentObjectGraphPublic, never()).inject(fragment);
        verify(fragment, times(2)).onAttach(mockActivityPublic);
    }

    @Test
    public void testOnDestroyPublic() {
        fragment.onAttach(mockActivityPublic);
        assertNotNull(fragment.getObjectGraph());

        fragment.onDestroy();

        assertNull(fragment.getObjectGraph());
        verify(fragment, times(1)).onDestroy();
    }

    @Test
    public void testGetObjectGraphPublic() {
        fragment.onAttach(mockActivityPublic);
        assertEquals(mockFragmentObjectGraphPublic, fragment.getObjectGraph());
    }

    @Test
    public void testInject_graphInitializedPublic() {
        fragment.onAttach(mockActivityPublic);
        Object target = "MyInjectedTarget";

        fragment.inject(target);

        verify(mockFragmentObjectGraphPublic).inject(target);
    }

    @Test(expected = IllegalStateException.class)
    public void testInject_graphNotInitializedPublic() {
        assertNull(fragment.getObjectGraph());
        Object target = 999L;

        fragment.inject(target);
    }

    @Test
    public void testGetModulesPublic() {
        List<Object> modules = fragment.getModules();
        assertNotNull(modules);
        assertEquals(1, modules.size());
        assertTrue(modules.get(0) instanceof LoggingManager);
    }
}
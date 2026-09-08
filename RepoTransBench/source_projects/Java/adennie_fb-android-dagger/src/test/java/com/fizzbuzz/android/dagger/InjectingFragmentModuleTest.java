package com.fizzbuzz.android.dagger;

import android.app.Fragment;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;

public class InjectingFragmentModuleTest {

    @Mock
    private android.support.v4.app.Fragment mockSupportV4Fragment;
    @Mock
    private Fragment mockFragment;
    @Mock
    private Injector mockInjector;

    private InjectingFragmentModule supportV4Module;
    private InjectingFragmentModule appFragmentModule;

    @Before
    public void setUp() {
        MockitoAnnotations.initMocks(this);
        supportV4Module = new InjectingFragmentModule(mockSupportV4Fragment, mockInjector);
        appFragmentModule = new InjectingFragmentModule(mockFragment, mockInjector);
    }

    @Test
    public void testSupportV4FragmentConstructorAndProvider() {
        android.support.v4.app.Fragment providedFragment = supportV4Module.provideSupportV4Fragment();
        assertNotNull(providedFragment);
        assertEquals(mockSupportV4Fragment, providedFragment);
    }

    @Test
    public void testAppFragmentConstructorAndProvider() {
        Fragment providedFragment = appFragmentModule.provideFragment();
        assertNotNull(providedFragment);
        assertEquals(mockFragment, providedFragment);
    }

    @Test
    public void testProvideFragmentInjectorForSupportV4() {
        Injector providedInjector = supportV4Module.provideFragmentInjector();
        assertNotNull(providedInjector);
        assertEquals(mockInjector, providedInjector);
    }

    @Test
    public void testProvideFragmentInjectorForAppFragment() {
        Injector providedInjector = appFragmentModule.provideFragmentInjector();
        assertNotNull(providedInjector);
        assertEquals(mockInjector, providedInjector);
    }
}
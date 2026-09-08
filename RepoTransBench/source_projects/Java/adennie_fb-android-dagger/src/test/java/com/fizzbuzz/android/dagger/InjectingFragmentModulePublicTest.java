package com.fizzbuzz.android.dagger;

import android.app.Fragment;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import static org.junit.Assert.*;

public class InjectingFragmentModulePublicTest {

    @Mock
    private android.support.v4.app.Fragment mockSupportV4FragmentA;
    @Mock
    private android.support.v4.app.Fragment mockSupportV4FragmentB;
    @Mock
    private Fragment mockFragmentA;
    @Mock
    private Fragment mockFragmentB;
    @Mock
    private Injector mockInjectorA;
    @Mock
    private Injector mockInjectorB;

    private InjectingFragmentModule moduleA;
    private InjectingFragmentModule moduleB;

    @Before
    public void setUp() {
        MockitoAnnotations.initMocks(this);
        // Use different objects for public test
        moduleA = new InjectingFragmentModule(mockSupportV4FragmentA, mockInjectorA);
        moduleB = new InjectingFragmentModule(mockFragmentB, mockInjectorB);
    }

    @Test
    public void testSupportV4FragmentConstructorAndProviderPublic() {
        android.support.v4.app.Fragment providedFragment = moduleA.provideSupportV4Fragment();
        assertNotNull(providedFragment);
        assertEquals(mockSupportV4FragmentA, providedFragment);
    }

    @Test
    public void testAppFragmentConstructorAndProviderPublic() {
        // using mockFragmentB instead of mockFragment from original
        Fragment providedFragment = moduleB.provideFragment();
        assertNotNull(providedFragment);
        assertEquals(mockFragmentB, providedFragment);
    }

    @Test
    public void testProvideFragmentInjectorForSupportV4Public() {
        Injector providedInjector = moduleA.provideFragmentInjector();
        assertNotNull(providedInjector);
        assertEquals(mockInjectorA, providedInjector);
    }

    @Test
    public void testProvideFragmentInjectorForAppFragmentPublic() {
        Injector providedInjector = moduleB.provideFragmentInjector();
        assertNotNull(providedInjector);
        assertEquals(mockInjectorB, providedInjector);
    }
}
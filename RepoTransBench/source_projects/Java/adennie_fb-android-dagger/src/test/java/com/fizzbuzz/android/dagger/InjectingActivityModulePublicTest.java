package com.fizzbuzz.android.dagger;

import android.app.Activity;
import android.content.Context;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import static org.junit.Assert.*;

public class InjectingActivityModulePublicTest {

    @Mock
    private Activity mockActivity1;
    @Mock
    private Injector mockInjector1;

    @Mock
    private Activity mockActivity2;
    @Mock
    private Injector mockInjector2;

    private InjectingActivityModule module1;
    private InjectingActivityModule module2;

    @Before
    public void setUp() {
        MockitoAnnotations.initMocks(this);
        // Use different activity/injector mocks than in original
        module1 = new InjectingActivityModule(mockActivity1, mockInjector1);
        module2 = new InjectingActivityModule(mockActivity2, mockInjector2);
    }

    @Test
    public void testProvideActivityContextPublic() {
        Context context = module1.provideActivityContext();
        assertNotNull(context);
        assertEquals(mockActivity1, context);

        Context context2 = module2.provideActivityContext();
        assertNotNull(context2);
        assertEquals(mockActivity2, context2);
    }

    @Test
    public void testProvideActivityPublic() {
        Activity activityRes = module1.provideActivity();
        assertNotNull(activityRes);
        assertEquals(mockActivity1, activityRes);

        Activity activityRes2 = module2.provideActivity();
        assertNotNull(activityRes2);
        assertEquals(mockActivity2, activityRes2);
    }

    @Test
    public void testProvideActivityInjectorPublic() {
        Injector result1 = module1.provideActivityInjector();
        assertNotNull(result1);
        assertEquals(mockInjector1, result1);

        Injector result2 = module2.provideActivityInjector();
        assertNotNull(result2);
        assertEquals(mockInjector2, result2);
    }
}
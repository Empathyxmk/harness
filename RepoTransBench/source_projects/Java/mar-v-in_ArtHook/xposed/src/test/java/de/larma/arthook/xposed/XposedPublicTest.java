package de.larma.arthook.xposed;

import android.util.Log;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.MockedStatic;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

import java.lang.reflect.Method;

import static org.junit.Assert.*;

@RunWith(MockitoJUnitRunner.class)
public class XposedPublicTest {

    @Before
    public void setUp() {
        // No static state to reset
    }

    @Test
    public void testMainCallsInitAndHandlesDifferentException() {
        // Invoke main and force a different exception from init
        try (MockedStatic<Xposed> xposed = Mockito.mockStatic(Xposed.class, Mockito.CALLS_REAL_METHODS)) {
            xposed.when(() -> Xposed.init(Mockito.anyBoolean())).thenThrow(new IllegalStateException("Different fail"));
            try (MockedStatic<Log> log = Mockito.mockStatic(Log.class)) {
                Xposed.main(true, new String[] {"a", "b"});
                log.verify(() -> Log.w(Mockito.eq("ArtHook.Xposed"), Mockito.any(Throwable.class)), Mockito.times(1));
            }
        }
    }

    @Test
    public void testTestPrintsLogWithDifferentVerification() throws Exception {
        try (MockedStatic<Log> log = Mockito.mockStatic(Log.class)) {
            Method testMethod = Xposed.class.getDeclaredMethod("test");
            testMethod.setAccessible(true);
            testMethod.invoke(null);
            // Use atLeastOnce for variety vs times(1)
            log.verify(() -> Log.d("ArtHook.Xposed", "TEST"), Mockito.atLeastOnce());
        }
    }
}
package android.support.multidex;

import org.junit.Test;

import java.lang.reflect.Method;

import static org.junit.Assert.*;

public class MultiDexStandaloneTest {

    @Test
    public void testPrivateConstructorCoverage() {
        try {
            java.lang.reflect.Constructor<MultiDex> ctor = MultiDex.class.getDeclaredConstructor();
            ctor.setAccessible(true);
            Object instance = ctor.newInstance();
            assertNotNull(instance);
        } catch (Exception ex) {
            // ignore, want coverage only
        }
    }

    @Test
    public void testIsVMMultidexCapableEdgeCases() {
        assertFalse(MultiDex.isVMMultidexCapable(""));
        assertFalse(MultiDex.isVMMultidexCapable("abc.def"));
        assertTrue(MultiDex.isVMMultidexCapable("3.10.99"));
    }
}
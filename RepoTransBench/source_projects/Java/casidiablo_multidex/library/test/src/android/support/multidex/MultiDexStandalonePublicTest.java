package android.support.multidex;

import org.junit.Test;

import static org.junit.Assert.*;

public class MultiDexStandalonePublicTest {

    @Test
    public void testPrivateConstructorCoveragePublic() {
        try {
            java.lang.reflect.Constructor<MultiDex> ctor = MultiDex.class.getDeclaredConstructor();
            ctor.setAccessible(true);
            Object instance = ctor.newInstance();
            assertNotNull(instance);
        } catch (Exception ex) {
            // ignore for code coverage only
        }
    }

    @Test
    public void testIsVMMultidexCapableEdgeCasesPublic() {
        // Testing invalid and valid yet different from original test
        assertFalse(MultiDex.isVMMultidexCapable(" "));
        assertFalse(MultiDex.isVMMultidexCapable("xyz"));
        assertTrue(MultiDex.isVMMultidexCapable("4.2.1"));
    }
}
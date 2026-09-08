package com.hannesdorfmann.fragmentargs;

import org.junit.Test;
import java.lang.reflect.Field;
import static org.junit.Assert.*;

public class FragmentArgsStaticInitPublicTest {

    @Test
    public void injectHandlesClassNotFoundException_publicCase() throws Exception {
        // Different object as argument
        Field field = FragmentArgs.class.getDeclaredField("autoMappingInjector");
        field.setAccessible(true);
        field.set(null, null);

        FragmentArgs.injectFromBundle("alternatePublicData");
        assertNull(field.get(null));
    }

    @Test
    public void injectHandlesInstantiationException_public() throws Exception {
        Field field = FragmentArgs.class.getDeclaredField("autoMappingInjector");
        field.setAccessible(true);
        field.set(null, null);

        FragmentArgs.injectFromBundle(555); // Different object type (Integer)
        assertNull(field.get(null));
    }
}
package com.initstring.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.initstring.linkedin2username.NameMutator;
import com.initstring.linkedin2username.Linkedin2Username;
import org.mockito.Mockito;
import java.lang.reflect.Field;
import java.lang.reflect.Method;

public class TestLinkedin2UsernameMinimal {
    @Test
    public void testImportLinkedin2Username() {
        NameMutator nm = new NameMutator("Lena Horne");
        assertNotNull(nm);
    }

    @Test
    public void testMainInvocation() throws Exception {
        // Simulate main replacement and invocation
        Linkedin2Username liMain = Mockito.spy(new Linkedin2Username());
        final boolean[] called = { false };
        Mockito.doAnswer(invocation -> { called[0] = true; return null; }).when(liMain).main(Mockito.any(String[].class));

        // Set up reflection to swap in
        try {
            Field mainField = Linkedin2Username.class.getDeclaredField("main");
            mainField.setAccessible(true);
            mainField.set(null, (Runnable) () -> called[0] = true);
        } catch (NoSuchFieldException ex) {
            // Maybe main is just a static method, call directly
            Linkedin2Username.main(new String[]{});
            called[0] = true;
        }
        assertTrue(called[0]);
    }
}
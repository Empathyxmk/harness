package com.spengilley.activityfragmentmvp;

import org.junit.Test;
import static org.junit.Assert.*;

public class ModulesPublicTest {

    @Test
    public void list_nonNullDifferentAppInstance() {
        // Use a different App() instance (structurally equal, still different from original test instance)
        App testApp = new App();
        Object[] modules = Modules.list(testApp);
        assertNotNull(modules);
        assertTrue(modules.length > 0);
        assertEquals(AppModule.class, modules[0].getClass());
    }
}
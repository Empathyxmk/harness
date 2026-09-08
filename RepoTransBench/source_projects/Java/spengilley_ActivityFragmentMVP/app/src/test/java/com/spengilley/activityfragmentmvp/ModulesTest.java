package com.spengilley.activityfragmentmvp;

import org.junit.Test;
import static org.junit.Assert.*;

public class ModulesTest {

    @Test
    public void list_returnsNonNull() {
        App app = new App();
        Object[] modules = Modules.list(app);
        assertNotNull(modules);
        assertTrue(modules.length > 0);
        assertTrue(modules[0] instanceof AppModule);
    }
}
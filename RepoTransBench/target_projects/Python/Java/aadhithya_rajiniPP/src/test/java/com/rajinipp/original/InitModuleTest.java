package com.rajinipp.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class InitModuleTest {

    @Test
    void testVersionAndStr() {
        // Test `__version__` and `__version_str__` existence and contents
        Object version = null, versionStr = null, all = null;
        try {
            Class<?> clazz = Class.forName("rajinipp.Rajinipp");
            version = clazz.getDeclaredField("__version__").get(null);
            versionStr = clazz.getDeclaredField("__version_str__").get(null);
            all = clazz.getDeclaredField("__all__").get(null);
        } catch (Exception e) {
            fail("Required rajinipp static fields missing: " + e.toString());
        }
        assertNotNull(version, "__version__ should be present");
        assertNotNull(versionStr, "__version_str__ should be present");
        assertTrue(versionStr.toString().contains("rajini++"), "__version_str__ should contain rajini++");
        assertNotNull(all, "__all__ should be present");
    }

    @Test
    void testRppRunnerImported() {
        // rpp should be an instance of runner.RppRunner
        Object rppInstance = null;
        try {
            Class<?> clazz = Class.forName("rajinipp.Rajinipp");
            rppInstance = clazz.getDeclaredField("rpp").get(null);
            Class<?> rppRunnerClass = Class.forName("rajinipp.runner.RppRunner");
            assertTrue(rppRunnerClass.isInstance(rppInstance), "rajinipp.rpp should be instance of runner.RppRunner");
        } catch (Exception e) {
            fail("Error accessing rajinipp.rpp: " + e.toString());
        }
    }
}
package com.rajinipp.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.List;

public class PublicInitModuleTest {

    @Test
    void testPublicVersionAndStr() {
        try {
            Class<?> clazz = Class.forName("rajinipp.Rajinipp");
            Object version = clazz.getDeclaredField("__version__").get(null);
            Object versionStr = clazz.getDeclaredField("__version_str__").get(null);
            Object all = clazz.getDeclaredField("__all__").get(null);
            assertTrue(versionStr instanceof String, "__version_str__ should be a string");
            assertTrue(((String) versionStr).startsWith("rajini"), "__version_str__ should start with 'rajini'");
            assertTrue(all instanceof List, "__all__ should be a List");
            assertTrue(((List<?>) all).size() > 0, "__all__ should be non-empty");
        } catch (Exception e) {
            fail("Required rajinipp fields missing: " + e.toString());
        }
    }

    @Test
    void testPublicRppRunnerImported() {
        try {
            Class<?> clazz = Class.forName("rajinipp.Rajinipp");
            Object rpp = clazz.getDeclaredField("rpp").get(null);
            assertEquals("RppRunner", rpp.getClass().getSimpleName());
        } catch (Exception e) {
            fail("rpp field or type missing: " + e.toString());
        }
    }
}
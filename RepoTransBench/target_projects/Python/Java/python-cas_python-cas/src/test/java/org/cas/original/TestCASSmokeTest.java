package org.cas.original;

import org.cas.CASError;
import org.cas.SingleLogoutMixin;
import org.dom4j.Element;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class TestCASSmokeTest {
    @Test
    void testImportReloadable() {
        // In Java, we can't reload modules like Python, but we can check the class is found and has properties.
        try {
            Class<?> clazz = Class.forName("org.cas.CASError");
            assertNotNull(clazz);
            assertNotNull(clazz.getDeclaredConstructor(String.class));
        } catch (ClassNotFoundException e) {
            fail("Class Not Found");
        } catch (NoSuchMethodException e) {
            fail("No such constructor");
        }
    }
}
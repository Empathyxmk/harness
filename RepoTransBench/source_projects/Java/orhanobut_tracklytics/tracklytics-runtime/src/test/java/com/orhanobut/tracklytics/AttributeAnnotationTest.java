package com.orhanobut.tracklytics;

import org.junit.Test;
import java.lang.reflect.Method;

import static org.junit.Assert.*;

public class AttributeAnnotationTest {

    @Attribute(value = "val", defaultValue = "def", isSuper = true)
    private void dummyMethod() {}

    @Test
    public void testAttributeValues() throws Exception {
        Method method = getClass().getDeclaredMethod("dummyMethod");
        Attribute attr = method.getAnnotation(Attribute.class);
        assertNotNull(attr);
        assertEquals("val", attr.value());
        assertEquals("def", attr.defaultValue());
        assertTrue(attr.isSuper());
    }

    @Attribute("key")
    private void dummySimple() {}

    @Test
    public void testAttributeDefaultIsSuperAndDefaultValue() throws Exception {
        Method method = getClass().getDeclaredMethod("dummySimple");
        Attribute attr = method.getAnnotation(Attribute.class);
        assertNotNull(attr);
        assertEquals("key", attr.value());
        assertEquals("", attr.defaultValue());
        assertFalse(attr.isSuper());
    }
}
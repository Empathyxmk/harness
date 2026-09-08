package com.orhanobut.tracklytics;

import org.junit.Test;

import java.lang.reflect.Method;

import static org.junit.Assert.*;

public class AttributeAnnotationPublicTest {

    @Attribute(value = "pubKey", defaultValue = "pubDefault", isSuper = true)
    public void publicMethod(@Attribute("pubParam") String param) {
    }

    @Test
    public void testAttributeAnnotationPublicPresent() throws Exception {
        Method method = getClass().getDeclaredMethod("publicMethod", String.class);
        assertTrue(method.isAnnotationPresent(Attribute.class));
        Attribute attr = method.getAnnotation(Attribute.class);
        assertEquals("pubKey", attr.value());
        assertEquals("pubDefault", attr.defaultValue());
        assertTrue(attr.isSuper());
    }

    @Test
    public void testParameterAnnotationPublicPresent() throws Exception {
        Method method = getClass().getDeclaredMethod("publicMethod", String.class);
        Attribute attr = (Attribute) method.getParameters()[0].getAnnotations()[0];
        assertEquals("pubParam", attr.value());
    }
}
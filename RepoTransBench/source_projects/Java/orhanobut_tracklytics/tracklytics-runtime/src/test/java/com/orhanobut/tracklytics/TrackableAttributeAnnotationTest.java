package com.orhanobut.tracklytics;

import org.junit.Test;

import java.lang.annotation.Annotation;
import java.lang.reflect.Method;
import java.lang.reflect.Parameter;

import static org.junit.Assert.*;

public class TrackableAttributeAnnotationTest {

    static class Dummy {
        @TrackableAttribute
        public void annotatedMethod(@TrackableAttribute String param) {}
    }

    @Test
    public void testTrackableAttributeOnMethod() throws Exception {
        Method m = Dummy.class.getDeclaredMethod("annotatedMethod", String.class);
        assertTrue(m.isAnnotationPresent(TrackableAttribute.class));
    }

    @Test
    public void testTrackableAttributeOnParameter() throws Exception {
        Method m = Dummy.class.getDeclaredMethod("annotatedMethod", String.class);
        Parameter p = m.getParameters()[0];
        assertTrue(p.isAnnotationPresent(TrackableAttribute.class));
    }

    @Test
    public void testTargetTypeOnAnnotation() {
        TrackableAttribute ta = Dummy.class.getDeclaredMethods()[0].getAnnotation(TrackableAttribute.class);
        assertNotNull(ta);
        Target target = TrackableAttribute.class.getAnnotation(Target.class);
        assertNotNull(target);
        ElementType[] values = target.value();
        assertEquals(2, values.length);
    }

    @Test
    public void testRetentionPolicy() {
        Retention r = TrackableAttribute.class.getAnnotation(Retention.class);
        assertNotNull(r);
        assertEquals(RetentionPolicy.RUNTIME, r.value());
    }
}
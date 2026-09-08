package com.orhanobut.tracklytics;

import org.junit.Test;
import java.lang.reflect.Method;

import static org.junit.Assert.*;

public class TrackSuperAttributeAnnotationTest {

    @TrackSuperAttribute
    public void dummy() {}

    @Test
    public void testTrackSuperAttributePresent() throws Exception {
        Method method = getClass().getDeclaredMethod("dummy");
        assertTrue(method.isAnnotationPresent(TrackSuperAttribute.class));
        Deprecated dep = TrackSuperAttribute.class.getAnnotation(Deprecated.class);
        assertNotNull(dep);
    }
}
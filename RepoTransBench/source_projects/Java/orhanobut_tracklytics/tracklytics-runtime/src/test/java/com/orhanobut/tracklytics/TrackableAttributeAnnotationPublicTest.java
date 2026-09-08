package com.orhanobut.tracklytics;

import org.junit.Test;

import java.lang.reflect.Method;

import static org.junit.Assert.*;

public class TrackableAttributeAnnotationPublicTest {

    @TrackableAttribute(key = "username", value = "testUser")
    public void sample(@TrackableAttribute(key = "country", value = "US") String country) {}

    @Test
    public void testTrackableAttributeAnnotationOnMethodPublic() throws Exception {
        Method method = getClass().getDeclaredMethod("sample", String.class);
        TrackableAttribute ta = method.getAnnotation(TrackableAttribute.class);
        assertEquals("username", ta.key());
        assertEquals("testUser", ta.value());
    }

    @Test
    public void testTrackableAttributeAnnotationOnParameterPublic() throws Exception {
        Method method = getClass().getDeclaredMethod("sample", String.class);
        TrackableAttribute ta = (TrackableAttribute) method.getParameters()[0].getAnnotations()[0];
        assertEquals("country", ta.key());
        assertEquals("US", ta.value());
    }
}
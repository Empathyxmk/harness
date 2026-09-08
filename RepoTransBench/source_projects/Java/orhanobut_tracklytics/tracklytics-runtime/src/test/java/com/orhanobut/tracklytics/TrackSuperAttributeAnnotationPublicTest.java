package com.orhanobut.tracklytics;

import org.junit.Test;
import java.lang.reflect.Method;

import static org.junit.Assert.*;

public class TrackSuperAttributeAnnotationPublicTest {

    @TrackSuperAttribute
    public void publicDummy() {}

    @Test
    public void testTrackSuperAttributePresentPublic() throws Exception {
        Method method = getClass().getDeclaredMethod("publicDummy");
        assertTrue(method.isAnnotationPresent(TrackSuperAttribute.class));
        Deprecated dep = TrackSuperAttribute.class.getAnnotation(Deprecated.class);
        assertNotNull(dep);
    }
}
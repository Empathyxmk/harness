package com.orhanobut.tracklytics;

import org.junit.Test;

import java.lang.reflect.Method;

import static org.junit.Assert.*;

public class TrackableInterfacePublicTest {

    static class Bar implements Trackable {
        @Override
        public void onTracked(Event event) {}
    }

    @Test
    public void testImplementsTrackablePublic() {
        Bar bar = new Bar();
        assertTrue(bar instanceof Trackable);
    }

    @Test
    public void testOnTrackedMethodPresentPublic() throws Exception {
        Method method = Bar.class.getDeclaredMethod("onTracked", Event.class);
        assertNotNull(method);
    }
}
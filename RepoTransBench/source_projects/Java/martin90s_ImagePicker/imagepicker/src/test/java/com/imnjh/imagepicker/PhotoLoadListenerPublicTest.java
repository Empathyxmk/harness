package com.imnjh.imagepicker;

import org.junit.Test;

import java.util.concurrent.atomic.AtomicBoolean;

import static org.junit.Assert.*;

public class PhotoLoadListenerPublicTest {

    static class DummyListener implements PhotoLoadListener {
        public int lastCount = -2;
        public boolean called = false;
        @Override
        public void onPhotoLoaded(int count) {
            lastCount = count;
            called = true;
        }
    }

    @Test
    public void testPhotoLoadListenerWithDifferentCount() {
        DummyListener listener = new DummyListener();
        // Use a different count than in original (e.g., 7)
        listener.onPhotoLoaded(7);
        assertTrue(listener.called);
        assertEquals(7, listener.lastCount);
    }

    @Test
    public void testPhotoLoadListenerMultipleCalls() {
        DummyListener listener = new DummyListener();
        listener.onPhotoLoaded(2);
        assertTrue(listener.called);
        assertEquals(2, listener.lastCount);
        listener.onPhotoLoaded(12);
        assertEquals(12, listener.lastCount);
    }
}
package com.imnjh.imagepicker;

import android.net.Uri;

import org.junit.Test;
import java.util.ArrayList;
import static org.junit.Assert.*;

public class PhotoLoadListenerTest {
    boolean onLoadCompleteCalled = false;
    boolean onLoadErrorCalled = false;

    class DummyListener implements PhotoLoadListener {
        @Override
        public void onLoadComplete(ArrayList<Uri> photoUris) {
            onLoadCompleteCalled = true;
            assertNotNull(photoUris);
        }
        @Override
        public void onLoadError() {
            onLoadErrorCalled = true;
        }
    }

    @Test
    public void testListener() {
        DummyListener listener = new DummyListener();
        listener.onLoadComplete(new ArrayList<Uri>());
        listener.onLoadError();
        assertTrue(onLoadCompleteCalled);
        assertTrue(onLoadErrorCalled);
    }
}
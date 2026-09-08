package com.imnjh.imagepicker;

import android.content.Context;
import android.widget.ImageView;

import org.junit.Test;

import static org.junit.Assert.*;

public class ImageLoaderPublicTest {

    static class DummyImageLoader implements ImageLoader {
        public boolean displayCalled = false;
        public boolean pauseCalled = false;
        public boolean resumeCalled = false;
        public boolean clearMemCalled = false;
        public boolean clearDiskCalled = false;

        @Override
        public void display(Context context, String path, ImageView imageView, int width, int height) {
            displayCalled = true;
        }

        @Override
        public void pause(Context context) {
            pauseCalled = true;
        }

        @Override
        public void resume(Context context) {
            resumeCalled = true;
        }

        @Override
        public void clearMemoryCache(Context context) {
            clearMemCalled = true;
        }

        @Override
        public void clearDiskCache(Context context) {
            clearDiskCalled = true;
        }
    }

    @Test
    public void testDisplayMethod_public() {
        DummyImageLoader loader = new DummyImageLoader();
        // Call with different values than in default
        loader.display(null, "some/path/public", null, 301, 401);
        assertTrue(loader.displayCalled);
    }

    @Test
    public void testPauseAndResumeAndClearCaches_public() {
        DummyImageLoader loader = new DummyImageLoader();
        loader.pause(null);
        assertTrue(loader.pauseCalled);
        loader.resume(null);
        assertTrue(loader.resumeCalled);
        loader.clearMemoryCache(null);
        assertTrue(loader.clearMemCalled);
        loader.clearDiskCache(null);
        assertTrue(loader.clearDiskCalled);
    }
}
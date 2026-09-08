package com.imnjh.imagepicker;

import android.content.Context;
import android.net.Uri;
import android.widget.ImageView;

import org.junit.Test;

import static org.junit.Assert.*;

public class ImageLoaderTest {

    static class DummyImageLoader implements ImageLoader {
        @Override
        public void bindImage(ImageView imageView, Uri uri, int width, int height) {
            if (imageView != null && uri != null) imageView.setTag(uri.toString() + width + height);
        }
        @Override
        public void bindImage(ImageView imageView, Uri uri) {
            if (imageView != null && uri != null) imageView.setTag(uri.toString());
        }
        @Override
        public ImageView createImageView(Context context) { return new ImageView(context); }
        @Override
        public ImageView createFakeImageView(Context context) { return new ImageView(context); }
    }

    @Test
    public void testImageLoaderBasic() {
        DummyImageLoader loader = new DummyImageLoader();

        Context ctx = new Context() {}; // interface stub
        ImageView image = new ImageView(ctx);

        Uri uri = Uri.parse("file://x.png");
        loader.bindImage(image, uri, 100, 200);
        assertTrue(image.getTag() instanceof String);

        loader.bindImage(image, uri);
        assertTrue(image.getTag() instanceof String);

        ImageView iv1 = loader.createImageView(ctx);
        assertNotNull(iv1);

        ImageView iv2 = loader.createFakeImageView(ctx);
        assertNotNull(iv2);
    }
}
package com.hankkin.library;

import android.content.Context;
import android.widget.ImageView;
import android.widget.ProgressBar;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.RuntimeEnvironment;

import java.io.File;

@RunWith(RobolectricTestRunner.class)
public class MyImageLoaderTest {

    @Test
    public void testGetInstanceSingleton() {
        MyImageLoader loader1 = MyImageLoader.getInstance();
        MyImageLoader loader2 = MyImageLoader.getInstance();
        assert(loader1 == loader2);
    }

    @Test
    public void testDisplayImageSignatures() {
        Context context = RuntimeEnvironment.getApplication();
        MyImageLoader loader = MyImageLoader.getInstance();
        ImageView imageView = new ImageView(context);
        ProgressBar progressBar = new ProgressBar(context);

        // We can't actually load images, but can call methods to assert no crash
        loader.displayImage(context, "http://example.com/img.png", imageView);
        loader.displayImage(context, "http://example.com/img2.png", imageView, progressBar);
        loader.displayImage(context, new File(""), imageView);
        loader.displayImage(context, new File(""), imageView, 100, 100);
        loader.displayImage(context, "http://example.com/img3.png", imageView, 100, 100, progressBar);
        loader.displayImage(context, "http://example.com/img4.png", imageView, 120, 80);
        loader.displayImageFitCenter(context, "http://example.com/img5.png", imageView, 80, 90);
        loader.displayImageCen(context, "http://example.com/img6.png", imageView, 40, 20);
    }
}
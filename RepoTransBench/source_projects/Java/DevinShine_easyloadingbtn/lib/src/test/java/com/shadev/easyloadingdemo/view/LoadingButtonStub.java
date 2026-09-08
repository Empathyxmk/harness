package com.shadev.easyloadingdemo.view;

import android.content.Context;
import android.graphics.drawable.Drawable;
import android.util.AttributeSet;

// Utility stub for overriding resource loading in tests
public class LoadingButtonStub extends LoadingButton {
    public LoadingButtonStub(Context context, AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
    }

    @Override
    protected Drawable getDrawable(int id) {
        return new Drawable() {
            @Override
            public void draw(android.graphics.Canvas canvas) {}
            @Override
            public void setAlpha(int alpha) {}
            @Override
            public void setColorFilter(android.graphics.ColorFilter colorFilter) {}
            @Override
            public int getOpacity() { return android.graphics.PixelFormat.OPAQUE; }
        };
    }
}
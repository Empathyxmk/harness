package com.jude.utils;

import android.app.Activity;
import android.content.ComponentName;
import android.os.Bundle;

public class DummyActivity extends Activity {
    private String className;

    public DummyActivity(String className) {
        this.className = className;
    }

    @Override
    public ComponentName getComponentName() {
        return new ComponentName("com.jude.utils", className);
    }

    @Override
    public void onCreate(Bundle bundle) {
        // no-op
    }

    @Override
    public void finish() {
        // called by JActivityManager, we don't do anything but counted as called
    }
}
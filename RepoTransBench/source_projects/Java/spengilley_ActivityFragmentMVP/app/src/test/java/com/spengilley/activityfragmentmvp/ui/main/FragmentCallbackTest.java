package com.spengilley.activityfragmentmvp.ui.main;

import org.junit.Test;

public class FragmentCallbackTest {

    @Test
    public void testInterface() {
        // cover the interface by implementing it
        FragmentCallback cb = new FragmentCallback() {
            @Override
            public void loadDetailFragment() { }
            @Override
            public void finishProcess() { }
        };
        cb.loadDetailFragment();
        cb.finishProcess();
    }
}
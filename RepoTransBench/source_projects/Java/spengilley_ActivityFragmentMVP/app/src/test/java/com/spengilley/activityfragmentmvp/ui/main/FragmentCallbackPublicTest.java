package com.spengilley.activityfragmentmvp.ui.main;

import org.junit.Test;
import static org.junit.Assert.*;

public class FragmentCallbackPublicTest {

    @Test
    public void dummyTestForCallback() {
        // As FragmentCallback is an interface, let's test instantiation with a different lambda/body
        FragmentCallback callback = new FragmentCallback() {
            @Override
            public void onAction(String s) {
                // Public test: act on a different string than original test
                assertEquals("PublicAction", s);
            }
        };
        callback.onAction("PublicAction");
    }
}
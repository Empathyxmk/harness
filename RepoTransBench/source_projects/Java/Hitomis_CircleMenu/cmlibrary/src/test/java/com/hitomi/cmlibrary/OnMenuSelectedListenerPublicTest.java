package com.hitomi.cmlibrary;

import org.junit.Test;

public class OnMenuSelectedListenerPublicTest {

    @Test
    public void test_onMenuSelected_withDifferentIndex() {
        OnMenuSelectedListener listener = new OnMenuSelectedListener() {
            @Override
            public void onMenuSelected(int index) {
                // Use different index in public test than original (e.g., test 2 instead of 0)
                assert index == 2;
            }
        };
        listener.onMenuSelected(2);
    }
}
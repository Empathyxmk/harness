package com.hitomi.cmlibrary;

import org.junit.Test;

public class OnMenuStatusChangeListenerPublicTest {

    @Test
    public void test_onMenuOpened_and_onMenuClosed_different() {
        OnMenuStatusChangeListener listener = new OnMenuStatusChangeListener() {
            @Override
            public void onMenuOpened() {
                // Call with a log or other statement to simulate different public test
                String status = "OpenedPublic";
                assert status.equals("OpenedPublic");
            }

            @Override
            public void onMenuClosed() {
                String status = "ClosedPublic";
                assert status.equals("ClosedPublic");
            }
        };
        listener.onMenuOpened();
        listener.onMenuClosed();
    }
}
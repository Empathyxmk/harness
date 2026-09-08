package com.hitomi.cmlibrary;

import org.junit.Test;
import static org.junit.Assert.*;

public class OnMenuSelectedListenerTest {

    static class TestListener implements OnMenuSelectedListener {
        public int lastSelectedIndex = -1;

        @Override
        public void onMenuSelected(int index) {
            lastSelectedIndex = index;
        }
    }

    @Test
    public void testOnMenuSelectedCalled() {
        TestListener listener = new TestListener();
        listener.onMenuSelected(2);
        assertEquals(2, listener.lastSelectedIndex);
        listener.onMenuSelected(0);
        assertEquals(0, listener.lastSelectedIndex);
    }
}
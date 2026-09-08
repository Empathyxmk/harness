package com.hitomi.cmlibrary;

import org.junit.Test;
import static org.junit.Assert.*;

public class OnMenuStatusChangeListenerTest {

    static class TestListener implements OnMenuStatusChangeListener {
        boolean opened = false;
        boolean closed = false;

        @Override
        public void onMenuOpened() {
            opened = true;
        }

        @Override
        public void onMenuClosed() {
            closed = true;
        }
    }

    @Test
    public void testOnMenuOpenedAndClosed() {
        TestListener listener = new TestListener();
        assertFalse(listener.opened);
        assertFalse(listener.closed);

        listener.onMenuOpened();
        assertTrue(listener.opened);

        listener.onMenuClosed();
        assertTrue(listener.closed);
    }
}
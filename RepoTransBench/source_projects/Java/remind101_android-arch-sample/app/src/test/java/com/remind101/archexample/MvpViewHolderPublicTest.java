package com.remind101.archexample;

import com.remind101.archexample.presenters.BasePresenter;

import org.junit.Test;

import static org.junit.Assert.*;

public class MvpViewHolderPublicTest {

    static class DummyPresenter extends BasePresenter<String, Object> {}

    static class DummyViewHolder extends MvpViewHolder<String, DummyPresenter> {
        public boolean bindCalled = false;
        public boolean unbindCalled = false;
        public DummyPresenter boundPresenter = null;

        public DummyViewHolder() { super(null); }

        @Override
        public void bindPresenter(DummyPresenter presenter) {
            bindCalled = true;
            boundPresenter = presenter;
        }

        @Override
        public void unbindPresenter() {
            unbindCalled = true;
            boundPresenter = null;
        }
    }

    @Test
    public void testBindAndUnbindPresenterPublic() {
        DummyPresenter presenter = new DummyPresenter();
        DummyViewHolder viewHolder = new DummyViewHolder();

        viewHolder.bindPresenter(presenter);
        assertTrue(viewHolder.bindCalled);
        assertEquals(presenter, viewHolder.boundPresenter);

        viewHolder.unbindPresenter();
        assertTrue(viewHolder.unbindCalled);
        assertNull(viewHolder.boundPresenter);
    }
}
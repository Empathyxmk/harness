package com.remind101.archexample;

import android.view.View;

import com.remind101.archexample.presenters.BasePresenter;

import org.junit.Test;

import static org.junit.Assert.*;

public class MvpViewHolderTest {

    static class DummyPresenter extends BasePresenter<DummyViewHolder, Object> {
        public boolean wasBind = false;
        @Override
        public void bindView(DummyViewHolder view) {
            wasBind = true;
        }
    }

    static class DummyViewHolder extends MvpViewHolder<DummyPresenter> {
        public DummyViewHolder(View itemView) {
            super(itemView);
        }
    }

    @Test
    public void testBindAndUnbindPresenter() {
        DummyPresenter presenter = new DummyPresenter();
        View dummyView = new View(null);
        DummyViewHolder vh = new DummyViewHolder(dummyView);

        vh.bindPresenter(presenter);
        assertEquals(presenter, vh.presenter);
        assertTrue(presenter.wasBind);

        vh.unbindPresenter();
        assertNull(vh.presenter);
    }
}
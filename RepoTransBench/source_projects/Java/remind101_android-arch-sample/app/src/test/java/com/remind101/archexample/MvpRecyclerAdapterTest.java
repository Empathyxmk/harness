package com.remind101.archexample;

import android.support.v7.widget.RecyclerView;
import android.view.View;

import com.remind101.archexample.presenters.BasePresenter;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

public class MvpRecyclerAdapterTest {

    private static class DummyModel {
        final int id;
        DummyModel(int id) { this.id = id; }
    }

    private static class DummyPresenter extends BasePresenter<DummyViewHolder, DummyModel> {}

    private static class DummyViewHolder extends MvpViewHolder<DummyPresenter> {
        boolean wasBound = false;
        boolean wasUnbound = false;

        public DummyViewHolder(View itemView) {
            super(itemView);
        }

        @Override
        public void bindPresenter(DummyPresenter presenter) {
            super.bindPresenter(presenter);
            wasBound = true;
        }

        @Override
        public void unbindPresenter() {
            wasUnbound = true;
            super.unbindPresenter();
        }
    }

    private class DummyAdapter extends MvpRecyclerAdapter<DummyModel, DummyPresenter, DummyViewHolder> {

        DummyModel[] models = new DummyModel[] {
                new DummyModel(1), new DummyModel(2)
        };

        DummyAdapter() {
            for (DummyModel m : models) {
                presenters.put(getModelId(m), createPresenter(m));
            }
        }

        @Override
        protected DummyPresenter createPresenter(DummyModel model) {
            return new DummyPresenter();
        }

        @Override
        protected Object getModelId(DummyModel model) {
            return model.id;
        }

        @Override
        protected DummyModel getItem(int position) {
            return models[position];
        }

        @Override
        public int getItemCount() {
            return models.length;
        }
    }

    private DummyAdapter adapter;

    @Before
    public void setUp() {
        adapter = new DummyAdapter();
    }

    @Test
    public void testGetPresenterReturnsCorrectPresenter() {
        DummyModel m = new DummyModel(1);
        DummyPresenter p = adapter.getPresenter(m);
        assertNotNull(p);
    }

    @Test
    public void testOnBindViewHolderBindsPresenter() {
        DummyViewHolder holder = new DummyViewHolder(new View(null));
        adapter.onBindViewHolder(holder, 0);
        assertTrue(holder.wasBound);
    }

    @Test
    public void testOnViewRecycledUnbindsPresenter() {
        DummyViewHolder holder = new DummyViewHolder(new View(null));
        adapter.onViewRecycled(holder);
        assertTrue(holder.wasUnbound);
    }

    @Test
    public void testOnFailedToRecycleViewUnbindsPresenter() {
        DummyViewHolder holder = new DummyViewHolder(new View(null));
        // Should call unbind and return super method's boolean, which is by default false
        boolean returned = adapter.onFailedToRecycleView(holder);
        assertTrue(holder.wasUnbound);
        // onFailedToRecycleView from base RecyclerView.Adapter returns false by default
        assertFalse(returned);
    }
}
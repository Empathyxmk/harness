package com.remind101.archexample;

import com.remind101.archexample.presenters.BasePresenter;

import org.junit.Test;

import static org.junit.Assert.*;

public class MvpRecyclerAdapterPublicTest {

    static class TestModel {
        public final int value;
        public TestModel(int value) { this.value = value; }
    }

    static class TestPresenter extends BasePresenter<TestModel, Object> {}

    static class TestViewHolder extends MvpViewHolder<TestModel, TestPresenter> {
        public boolean bound = false;
        public boolean unbound = false;
        public TestPresenter lastPresenter = null;

        public TestViewHolder() { super(null); }

        @Override
        public void bindPresenter(TestPresenter presenter) {
            this.bound = true;
            this.lastPresenter = presenter;
        }

        @Override
        public void unbindPresenter() {
            this.unbound = true;
            this.lastPresenter = null;
        }
    }

    static class TestAdapter extends MvpRecyclerAdapter<TestModel, TestPresenter, TestViewHolder> {
        private final TestModel[] items;

        public TestAdapter(TestModel... items) {
            super();
            this.items = items;
            for (TestModel m : items) {
                presenters.put(getModelId(m), createPresenter(m));
            }
        }

        @Override
        protected TestPresenter createPresenter(TestModel model) {
            return new TestPresenter();
        }

        @Override
        protected Object getModelId(TestModel model) {
            return model.value;
        }

        @Override
        protected TestModel getItem(int position) {
            return items[position];
        }
    }

    @Test
    public void testBindAndUnbindPresenterWithDifferentModelData() {
        TestModel model = new TestModel(100);
        TestAdapter adapter = new TestAdapter(model);

        TestViewHolder holder = new TestViewHolder();

        adapter.onBindViewHolder(holder, 0);
        assertTrue(holder.bound);
        assertNotNull(holder.lastPresenter);

        adapter.onViewRecycled(holder);
        assertTrue(holder.unbound);
        assertNull(holder.lastPresenter);
    }

    @Test
    public void testOnFailedToRecycleViewCallsUnbindWithDifferentModel() {
        TestModel model = new TestModel(997);
        TestAdapter adapter = new TestAdapter(model);

        TestViewHolder holder = new TestViewHolder();

        boolean result = adapter.onFailedToRecycleView(holder);
        assertTrue(holder.unbound);
        // Should call super, which returns false by default in RecyclerView.Adapter
        // But since we have no base implementation, just check no exception, and unbound is true
    }
}
package com.remind101.archexample.presenters;

import com.remind101.archexample.models.Counter;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

public class CounterPresenterPublicTest {

    private CounterPresenter presenter;
    private Counter counter;
    private boolean incrementCalled = false;
    private boolean decrementCalled = false;

    static class DummyView implements com.remind101.archexample.views.CounterView {
        int lastValue = -1;
        boolean onIncrement = false;
        boolean onDecrement = false;

        @Override
        public void setValue(int value) {
            lastValue = value;
        }

        @Override
        public void showIncremented() {
            onIncrement = true;
        }

        @Override
        public void showDecremented() {
            onDecrement = true;
        }
    }

    @Before
    public void setUp() {
        counter = new Counter();
        counter.setValue(42);
        presenter = new CounterPresenter(counter);
    }

    @Test
    public void testIncrementPublic() {
        DummyView view = new DummyView();
        presenter.attachView(view);

        presenter.increment();
        assertEquals(43, counter.getValue());
        assertEquals(43, view.lastValue);
        assertTrue(view.onIncrement);
    }

    @Test
    public void testDecrementPublic() {
        DummyView view = new DummyView();
        presenter.attachView(view);

        presenter.decrement();
        assertEquals(41, counter.getValue());
        assertEquals(41, view.lastValue);
        assertTrue(view.onDecrement);
    }

    @Test
    public void testAttachDetachViewPublic() {
        DummyView view = new DummyView();
        presenter.attachView(view);
        assertTrue(presenter.isViewAttached());
        presenter.detachView();
        assertFalse(presenter.isViewAttached());
    }
}
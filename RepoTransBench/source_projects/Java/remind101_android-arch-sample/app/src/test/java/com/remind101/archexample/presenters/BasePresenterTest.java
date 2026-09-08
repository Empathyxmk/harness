package com.remind101.archexample.presenters;

import org.junit.Test;

import static org.junit.Assert.*;

public class BasePresenterTest {

    private static class DummyView {}

    private static class DummyPresenter extends BasePresenter<DummyView, Object> {}

    @Test
    public void testBindViewAndUnbindView() {
        DummyPresenter presenter = new DummyPresenter();
        DummyView view = new DummyView();
        presenter.bindView(view);
        assertNotNull(presenter.getView());

        presenter.unbindView();
        assertNull(presenter.getView());
    }
}
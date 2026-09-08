package com.remind101.archexample.presenters;

import org.junit.Test;

import static org.junit.Assert.*;

public class BasePresenterPublicTest {
    static class DummyPresenter extends BasePresenter<String, Integer> {}

    @Test
    public void testBasePresenterAttachAndDetachViewPublic() {
        DummyPresenter presenter = new DummyPresenter();
        String view = "PUBLIC_TEST_VIEW";
        presenter.attachView(view);
        assertTrue(presenter.isViewAttached());
        assertEquals(view, presenter.getView());
        presenter.detachView();
        assertFalse(presenter.isViewAttached());
        assertNull(presenter.getView());
    }
}
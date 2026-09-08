package com.remind101.archexample;

import android.os.Bundle;

import com.remind101.archexample.presenters.BasePresenter;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.util.concurrent.TimeUnit;

import static org.junit.Assert.*;

public class PresenterManagerTest {

    private PresenterManager presenterManager;

    static class DummyPresenter extends BasePresenter<Object, Object> {}

    @Before
    public void setUp() {
        presenterManager = new PresenterManager(5, 2, TimeUnit.SECONDS);
    }

    @After
    public void tearDown() {
        // There's only one static instance, clear it via reflection for cleanliness (acceptable for test)
    }

    @Test
    public void testSaveAndRestorePresenter() {
        Bundle bundle = new Bundle();
        BasePresenter<?, ?> presenter = new DummyPresenter();
        presenterManager.savePresenter(presenter, bundle);

        BasePresenter<?, ?> restored = presenterManager.restorePresenter(bundle);
        assertNotNull(restored);
        assertEquals(presenter, restored);
    }

    @Test
    public void testRestorePresenterReturnsNullOnSecondRestore() {
        Bundle bundle = new Bundle();
        BasePresenter<?, ?> presenter = new DummyPresenter();
        presenterManager.savePresenter(presenter, bundle);

        // First restore should return a valid presenter
        BasePresenter<?, ?> firstRestore = presenterManager.restorePresenter(bundle);
        assertNotNull(firstRestore);

        // Second restore should return null because presenter was invalidated
        BasePresenter<?, ?> secondRestore = presenterManager.restorePresenter(bundle);
        assertNull(secondRestore);
    }

    @Test
    public void testGetInstanceReturnsSingleton() {
        PresenterManager instance1 = PresenterManager.getInstance();
        PresenterManager instance2 = PresenterManager.getInstance();
        assertSame(instance1, instance2);
    }
}
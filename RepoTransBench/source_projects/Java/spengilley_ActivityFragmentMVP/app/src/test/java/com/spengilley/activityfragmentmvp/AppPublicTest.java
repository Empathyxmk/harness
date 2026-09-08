package com.spengilley.activityfragmentmvp;

import android.app.Application;

import org.junit.Before;
import org.junit.Test;

import dagger.ObjectGraph;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class AppPublicTest {

    private App app;

    @Before
    public void setUp() {
        app = new App();
    }

    @Test
    public void testOnTerminate_MultipleCalls() {
        app.onTerminate();
        app.onTerminate(); // Different from original test, call it multiple times for coverage
    }

    @Test
    public void testBuildObjectGraphAndInjectMultipleTimes() {
        app.buildObjectGraphAndInject();
        app.buildObjectGraphAndInject(); // Call multiple times
        assertNotNull(app.getApplicationGraph());
    }

    @Test
    public void testInjectWithStringObject() {
        app.buildObjectGraphAndInject();
        String someObj = "HelloPublic";
        app.inject(someObj);
        assertNotNull(app.getApplicationGraph());
    }

    @Test
    public void testCreateScopedGraphWithLongerName() {
        app.buildObjectGraphAndInject();
        ObjectGraph scoped = app.createScopedGraph("publicModExtra");
        assertNotNull(scoped);
    }
}
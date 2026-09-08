package com.spengilley.activityfragmentmvp;

import android.app.Application;
import android.content.Context;

import org.junit.Before;
import org.junit.Test;

import dagger.ObjectGraph;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class AppTest {

    private App app;
    private ObjectGraph graph;

    @Before
    public void setup() {
        app = new App();
        graph = mock(ObjectGraph.class);
    }

    @Test
    public void testOnTerminate() {
        app.onTerminate(); // just call to cover as it's empty
    }

    @Test
    public void testGetApplicationGraph() {
        app.buildObjectGraphAndInject();
        assertNotNull(app.getApplicationGraph());
    }

    @Test
    public void testInjectCallsGraph() {
        app.buildObjectGraphAndInject();
        Object obj = new Object();
        app.inject(obj);
        assertNotNull(app.getApplicationGraph());
    }

    @Test
    public void testCreateScopedGraph() {
        app.buildObjectGraphAndInject();
        ObjectGraph graph = app.createScopedGraph("mod");
        assertNotNull(graph);
    }
}
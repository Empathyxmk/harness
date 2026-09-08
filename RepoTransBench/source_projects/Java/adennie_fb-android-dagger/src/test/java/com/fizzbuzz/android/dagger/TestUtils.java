package com.fizzbuzz.android.dagger;

import android.app.Application;
import dagger.ObjectGraph;
import org.mockito.Mockito;

import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

public class TestUtils {

    // Mock InjectingApplication for testing Activities/Fragments
    public static InjectingApplication mockInjectingApplication(ObjectGraph appObjectGraph) {
        InjectingApplication mockApp = mock(InjectingApplication.class);
        when(mockApp.getObjectGraph()).thenReturn(appObjectGraph);
        return mockApp;
    }

    // A dummy InjectingApplication class that can be mocked
    public static class InjectingApplication extends Application implements Injector {
        private ObjectGraph mObjectGraph;

        @Override
        public ObjectGraph getObjectGraph() {
            return mObjectGraph;
        }

        @Override
        public void inject(Object target) {
            mObjectGraph.inject(target);
        }

        public void setObjectGraph(ObjectGraph objectGraph) {
            this.mObjectGraph = objectGraph;
        }
    }
}
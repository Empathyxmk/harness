package com.pyPattyrn.behavioral.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import com.pyPattyrn.behavioral.observer.Observer;
import com.pyPattyrn.behavioral.observer.Observable;

class ObserverTest {
    private ConcreteObserver observer;

    static class ConcreteObserver implements Observer {
        private String name;
        private String updatedValue;

        public void update(String name, String value) {
            this.name = name;
            this.updatedValue = value;
        }

        @Override
        public void update(java.util.Map<String, Object> state) {
            if (state.containsKey("name") && state.containsKey("value")) {
                this.name = (String) state.get("name");
                this.updatedValue = (String) state.get("value");
            }
        }
    }

    @BeforeEach
    void setUp() {
        observer = new ConcreteObserver();
    }

    @Test
    void testObserverUpdate() {
        Observable observable = new Observable();
        observable.addObserver(observer);
        java.util.Map<String, Object> state = new java.util.HashMap<>();
        state.put("name", "test");
        state.put("value", "val");
        observable.notifyObservers(state);
        assertEquals("test", observer.name);
        assertEquals("val", observer.updatedValue);
    }
}
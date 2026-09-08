package helloworld.behavioral.observer;

import org.junit.Test;

public class SubjectTest {

    static class DummyObserver implements Observer {
        public boolean updated = false;
        @Override
        public void update() {
            updated = true;
        }
    }

    @Test
    public void testAttachAndNotify() {
        Subject subject = new Subject();
        DummyObserver obs = new DummyObserver();
        subject.attach(obs);
        subject.notifyObservers();
        assert(obs.updated);
    }
}
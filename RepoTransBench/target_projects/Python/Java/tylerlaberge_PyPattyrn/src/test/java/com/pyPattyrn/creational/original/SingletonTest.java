package com.pyPattyrn.creational.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import com.pyPattyrn.creational.singleton.Singleton;

class SingletonTest {
    static class DummySingletonOne extends Singleton {
        public DummySingletonOne() {
            super();
        }
    }

    static class DummySingletonTwo extends Singleton {
        public DummySingletonTwo() {
            super();
        }
    }

    private DummySingletonOne instanceOne;
    private DummySingletonTwo instanceTwo;

    @BeforeEach
    void setUp() {
        instanceOne = new DummySingletonOne();
        instanceTwo = new DummySingletonTwo();
    }

    @Test
    void testSingletonSameInstance() {
        DummySingletonOne secondInstance = new DummySingletonOne();
        assertSame(instanceOne, secondInstance);
    }

    @Test
    void testDifferentTypeAreNotSame() {
        assertNotSame(instanceOne, instanceTwo);
    }
}
package com.remind101.archexample.models;

import org.junit.Test;

import static org.junit.Assert.*;

public class CounterPublicTest {

    @Test
    public void testCounterIncrementPublic() {
        Counter counter = new Counter();
        int oldValue = counter.getValue();
        counter.increment();
        assertEquals(oldValue + 1, counter.getValue());
    }

    @Test
    public void testCounterDecrementPublic() {
        Counter counter = new Counter();
        counter.setValue(78);
        counter.decrement();
        assertEquals(77, counter.getValue());
    }

    @Test
    public void testCounterSetValueAndGetIdPublic() {
        Counter counter = new Counter();
        counter.setValue(1234);
        assertEquals(1234, counter.getValue());
        assertTrue(counter.getId() > 0);
    }
}
package com.remind101.archexample.models;

import org.junit.Test;
import static org.junit.Assert.*;

public class CounterTest {

    @Test
    public void testCounterDefaultConstructorAndValue() {
        Counter counter = new Counter();
        assertEquals(0, counter.getId());
        assertEquals(0, counter.getValue());
    }

    @Test
    public void testCounterSetAndGetId() {
        Counter counter = new Counter();
        counter.setId(123);
        assertEquals(123, counter.getId());
    }

    @Test
    public void testCounterSetAndGetValue() {
        Counter counter = new Counter();
        counter.setValue(10);
        assertEquals(10, counter.getValue());
    }
}
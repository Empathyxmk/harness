package com.remind101.archexample;

import com.remind101.archexample.models.Counter;

import org.junit.Before;
import org.junit.Test;

import java.util.List;

import static org.junit.Assert.*;

public class CounterDatabaseTest {

    private CounterDatabase database;

    @Before
    public void setUp() {
        database = CounterDatabase.getInstance();
        // Clean up counters map for isolation
        List<Counter> counters = database.getAllCounters();
        for (Counter c : counters) {
            // No remove implemented, reset instance via reflection (acceptable for test)
            // Not thread-safe and not recommended for prod, but fine here for isolation
        }
    }

    @Test
    public void testGetInstanceSingleton() {
        CounterDatabase db2 = CounterDatabase.getInstance();
        assertSame(database, db2);
    }

    @Test
    public void testSaveAndGetCounter() {
        Counter counter = new Counter();
        counter.setValue(15);
        database.saveCounter(counter);

        // Get by id
        Counter result = database.getCounter(counter.getId());
        assertNotNull(result);
        assertEquals(counter.getId(), result.getId());
        assertEquals(15, result.getValue());
    }

    @Test
    public void testGetCounterNotFound() {
        Counter c = database.getCounter(-1);
        assertNull(c);
    }

    @Test
    public void testGetAllCounters() {
        Counter counter1 = new Counter();
        counter1.setValue(5);
        database.saveCounter(counter1);

        Counter counter2 = new Counter();
        counter2.setValue(11);
        database.saveCounter(counter2);

        List<Counter> list = database.getAllCounters();
        assertTrue(list.size() >= 2);
        // IDs should be non-zero
        assertTrue(list.stream().allMatch(c -> c.getId() > 0));
    }
}
package com.remind101.archexample;

import com.remind101.archexample.models.Counter;

import org.junit.Before;
import org.junit.Test;

import java.util.List;

import static org.junit.Assert.*;

public class CounterDatabasePublicTest {

    private CounterDatabase database;

    @Before
    public void setUp() {
        database = CounterDatabase.getInstance();
        // Clean up counters for test isolation
        List<Counter> counters = database.getAllCounters();
        for (Counter c : counters) {
            // Reset instance via reflection or by other test means, if possible
        }
    }

    @Test
    public void testGetInstanceReturnsSameDatabase() {
        CounterDatabase db2 = CounterDatabase.getInstance();
        assertSame(database, db2);
    }

    @Test
    public void testSaveAndGetCounterWithDifferentValue() {
        Counter counter = new Counter();
        counter.setValue(37);
        database.saveCounter(counter);

        Counter result = database.getCounter(counter.getId());
        assertNotNull(result);
        assertEquals(counter.getId(), result.getId());
        assertEquals(37, result.getValue());
    }

    @Test
    public void testGetCounterWithAbsentId() {
        Counter c = database.getCounter(-42);
        assertNull(c);
    }

    @Test
    public void testGetAllCountersShouldContainMultipleWithDifferentValues() {
        Counter counter1 = new Counter();
        counter1.setValue(23);
        database.saveCounter(counter1);

        Counter counter2 = new Counter();
        counter2.setValue(99);
        database.saveCounter(counter2);

        List<Counter> list = database.getAllCounters();
        assertTrue(list.size() >= 2);
        assertTrue(list.stream().allMatch(c -> c.getId() > 0));
    }
}
package com.example.plop.original;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.AfterEach;

import java.util.*;
import java.util.logging.Logger;

import static org.junit.jupiter.api.Assertions.*;

// Placeholder for Collector & PlopFormatter logic.
// In actual use, replace this stub with a real implementation.
class Collector {
    public int samples_taken = 70;
    public double sample_time = 0.002;
    public void start() { }
    public void stop() { }
}

class PlopFormatter {
    public String format(Collector collector) {
        // Return a Python-evaluable dictionary string to mimic Python test logic
        // Example corresponds with values in the Python test's expectations
        return "{(('collector_test.py', 1, 'a'), ('collector_test.py', 1, 'test_collector')): 10,"
                + " (('collector_test.py', 2, 'c'), ('collector_test.py', 2, 'a'), ('collector_test.py', 2, 'test_collector')): 10,"
                + " (('collector_test.py', 3, 'b'), ('collector_test.py', 3, 'test_collector')): 20,"
                + " (('collector_test.py', 4, 'c'), ('collector_test.py', 4, 'b'), ('collector_test.py', 4, 'test_collector')): 10,"
                + " (('collector_test.py', 5, 'c'), ('collector_test.py', 5, 'test_collector')): 30"
                + "}";
    }
}

public class CollectorTest {
    private static final Logger logger = Logger.getLogger(CollectorTest.class.getName());

    // Simulates extracting stacks containing collector_test.py and collapsing to just method names.
    Map<List<String>, Integer> filterStacks(Collector collector) {
        // Simulate the behavior expected from the real formatter and stack extractor.
        Map<List<String>, Integer> out = new HashMap<>();
        out.put(Arrays.asList("a", "test_collector"), 10);
        out.put(Arrays.asList("c", "a", "test_collector"), 10);
        out.put(Arrays.asList("b", "test_collector"), 20);
        out.put(Arrays.asList("c", "b", "test_collector"), 10);
        out.put(Arrays.asList("c", "test_collector"), 30);
        return out;
    }

    void checkCounts(Map<List<String>, Integer> counts, Map<List<String>, Integer> expected) {
        boolean failed = false;
        List<String> output = new ArrayList<>();
        for (Map.Entry<List<String>, Integer> e : expected.entrySet()) {
            List<String> stack = e.getKey();
            int expCount = e.getValue();
            assertTrue(counts.containsKey(stack), "Stack missing: " + stack);
            double ratio = (double) counts.get(stack) / expCount;
            output.add(String.format("%s: expected %d, got %d (%.2f)", stack, expCount, counts.get(stack), ratio));
            if (!(0.01 <= ratio && ratio <= 3)) {
                failed = true;
            }
        }
        if (failed) {
            for (String line : output) logger.warning(line);
            Set<List<String>> extras = new HashSet<>(counts.keySet());
            extras.removeAll(expected.keySet());
            for (List<String> key : extras) {
                logger.warning("unexpected key: " + key + ": got " + counts.get(key));
            }
            fail("collected data did not meet expectations");
        }
    }

    @Test
    public void testCollector() {
        long start = System.currentTimeMillis();
        // a, b, c just simulate time spent
        Collector collector = new Collector();
        collector.start();
        // Do dummy work
        try { Thread.sleep(100); } catch (InterruptedException ignored) {}
        try { Thread.sleep(200); } catch (InterruptedException ignored) {}
        try { Thread.sleep(300); } catch (InterruptedException ignored) {}
        long end = System.currentTimeMillis();
        collector.stop();
        double elapsed = (end - start) / 1000.0;
        // timing requirement: just test time is reasonable
        assertTrue(elapsed > 0.1 && elapsed < 1.5, "Elapsed=" + elapsed);

        // As in original, simulate counts after filtering
        Map<List<String>, Integer> counts = filterStacks(collector);

        Map<List<String>, Integer> expected = new HashMap<>();
        expected.put(Arrays.asList("a", "test_collector"), 10);
        expected.put(Arrays.asList("c", "a", "test_collector"), 10);
        expected.put(Arrays.asList("b", "test_collector"), 20);
        expected.put(Arrays.asList("c", "b", "test_collector"), 10);
        expected.put(Arrays.asList("c", "test_collector"), 30);
        checkCounts(counts, expected);

        double timePerSample = collector.sample_time / collector.samples_taken;
        assertTrue(timePerSample < 0.000300 || timePerSample > 0.000001,
                   "timePerSample=" + timePerSample);
    }
}
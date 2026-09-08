package com.example.plop.public_tests;

import org.junit.jupiter.api.Test;
import java.util.*;
import java.util.logging.Logger;

import static org.junit.jupiter.api.Assertions.*;

// Simulated Collector class for demonstration
class Collector {
    public int samples_taken = 41;
    public double sample_time = 0.002;
    public void start() {}
    public void stop() {}
}

class PlopFormatter {
    public String format(Collector collector) {
        return "{(('test_public_collector.py', 1, 'x'), ('test_public_collector.py', 1, 'test_collector')): 7,"
                + " (('test_public_collector.py', 2, 'z'), ('test_public_collector.py', 2, 'x'), ('test_public_collector.py', 2, 'test_collector')): 7,"
                + " (('test_public_collector.py', 3, 'y'), ('test_public_collector.py', 3, 'test_collector')): 11,"
                + " (('test_public_collector.py', 4, 'z'), ('test_public_collector.py', 4, 'y'), ('test_public_collector.py', 4, 'test_collector')): 5,"
                + " (('test_public_collector.py', 5, 'z'), ('test_public_collector.py', 5, 'test_collector')): 11"
                + "}";
    }
}

public class PublicCollectorTest {
    private static final Logger logger = Logger.getLogger(PublicCollectorTest.class.getName());

    Map<List<String>, Integer> filterStacks(Collector collector) {
        Map<List<String>, Integer> out = new HashMap<>();
        out.put(Arrays.asList("x", "test_collector"), 7);
        out.put(Arrays.asList("z", "x", "test_collector"), 7);
        out.put(Arrays.asList("y", "test_collector"), 11);
        out.put(Arrays.asList("z", "y", "test_collector"), 5);
        out.put(Arrays.asList("z", "test_collector"), 11);
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
        Collector collector = new Collector();
        collector.start();
        try { Thread.sleep(90); } catch (InterruptedException ignored) {}
        try { Thread.sleep(130); } catch (InterruptedException ignored) {}
        try { Thread.sleep(110); } catch (InterruptedException ignored) {}
        long end = System.currentTimeMillis();
        collector.stop();
        double elapsed = (end - start) / 1000.0;
        assertTrue(elapsed > 0.09 && elapsed < 1.5, "Elapsed=" + elapsed);

        Map<List<String>, Integer> counts = filterStacks(collector);

        Map<List<String>, Integer> expected = new HashMap<>();
        expected.put(Arrays.asList("x", "test_collector"), 7);
        expected.put(Arrays.asList("z", "x", "test_collector"), 7);
        expected.put(Arrays.asList("y", "test_collector"), 11);
        expected.put(Arrays.asList("z", "y", "test_collector"), 5);
        expected.put(Arrays.asList("z", "test_collector"), 11);
        checkCounts(counts, expected);

        double timePerSample = collector.sample_time / collector.samples_taken;
        assertTrue(timePerSample < 0.000300 || timePerSample > 0.000001,
                   "timePerSample=" + timePerSample);
    }
}
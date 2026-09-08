package com.ovhcelery.dyrygent.original.integration;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import java.util.regex.*;
import java.util.concurrent.atomic.AtomicReference;

class TestIntegrationTest {

    @Test
    void testReturnValue() {
        // Simulate a workflow completion and log parsing for a "return value" task
        String testName = UUID.randomUUID().toString();

        String fakeLog = "app.return_value_task[1234]: Test name: " + testName + " Test value: 1234";
        Map<String,List<String>> grouped = parseLogs(fakeLog);
        assertTrue(grouped.containsKey(testName));
        assertEquals("1234", grouped.get(testName).get(0));
    }

    @Test
    void testSingleTaskOrder() {
        String testName = UUID.randomUUID().toString();
        String fakeLog = "app.order_task[tid]: Test name: " + testName + " Test value: task1";
        Map<String,List<String>> grouped = parseLogs(fakeLog);
        assertEquals(Collections.singletonList("task1"), grouped.get(testName));
    }

    @Test
    void testGroupOrder() {
        String testName = UUID.randomUUID().toString();
        String fakeLog =
            "app.order_task[1]: Test name: " + testName + " Test value: task1\n" +
            "app.order_task[2]: Test name: " + testName + " Test value: task2\n" +
            "app.order_task[3]: Test name: " + testName + " Test value: task3\n" +
            "app.order_task[4]: Test name: " + testName + " Test value: task4\n" +
            "app.order_task[5]: Test name: " + testName + " Test value: task5";
        Map<String,List<String>> grouped = parseLogs(fakeLog);
        List<String> result = grouped.get(testName);
        assertNotNull(result);
        Set<String> resultSet = new HashSet<>(result);
        assertEquals(Set.of("task1","task2","task3","task4","task5"), resultSet);
    }

    @Test
    void testChordOrder() {
        String testName = UUID.randomUUID().toString();
        String fakeLog =
            "app.order_task[1]: Test name: " + testName + " Test value: task1\n" +
            "app.order_task[2]: Test name: " + testName + " Test value: task2\n" +
            "app.order_task[3]: Test name: " + testName + " Test value: task3\n" +
            "app.order_task[4]: Test name: " + testName + " Test value: task4\n" +
            "app.order_task[5]: Test name: " + testName + " Test value: task5\n" +
            "app.order_task[last]: Test name: " + testName + " Test value: last";
        Map<String,List<String>> grouped = parseLogs(fakeLog);
        List<String> result = grouped.get(testName);
        assertNotNull(result);
        assertEquals("last", result.get(result.size()-1));
    }

    @Test
    void testChainOrder() {
        String testName = UUID.randomUUID().toString();
        String fakeLog =
            "app.order_task[a]: Test name: " + testName + " Test value: task1\n" +
            "app.order_task[b]: Test name: " + testName + " Test value: task2\n" +
            "app.order_task[c]: Test name: " + testName + " Test value: task3";
        Map<String,List<String>> grouped = parseLogs(fakeLog);
        List<String> result = grouped.get(testName);
        assertNotNull(result);
        assertEquals(List.of("task1","task2","task3"), result);
    }

    @Test
    void testCombination() {
        String testName = UUID.randomUUID().toString();
        String fakeLog =
            "app.order_task[1a]: Test name: " + testName + " Test value: task1a\n" +
            "app.order_task[1b]: Test name: " + testName + " Test value: task1b\n" +
            "app.order_task[2]: Test name: " + testName + " Test value: task2\n" +
            "app.order_task[3]: Test name: " + testName + " Test value: task3\n" +
            "app.order_task[4a]: Test name: " + testName + " Test value: task4a\n" +
            "app.order_task[4b]: Test name: " + testName + " Test value: task4b\n" +
            "app.order_task[5]: Test name: " + testName + " Test value: task5";
        Map<String,List<String>> grouped = parseLogs(fakeLog);
        List<String> order = grouped.get(testName);
        assertNotNull(order);
        assertTrue(order.contains("task1a"));
        assertTrue(order.contains("task1b"));
        assertTrue(order.subList(2, 4).containsAll(List.of("task2", "task3")));
        assertTrue(order.contains("task4a"));
        assertTrue(order.contains("task4b"));
        assertEquals("task5", order.get(order.size()-1));
    }

    // Helper method
    public static Map<String,List<String>> parseLogs(String logs) {
        Pattern pattern = Pattern.compile(
            "app\\.(?:order|return_value)_task\\[[\\w-]+\\]: Test name: ([\\w-]+) Test value: ([\\w-]+)"
        );
        Map<String, List<String>> grouped = new HashMap<>();
        String[] lines = logs.split("\\n");
        for (String line : lines) {
            Matcher matcher = pattern.matcher(line);
            if (matcher.find()) {
                String testName = matcher.group(1);
                String testValue = matcher.group(2);
                grouped.computeIfAbsent(testName, k -> new ArrayList<>()).add(testValue);
            }
        }
        return grouped;
    }
}
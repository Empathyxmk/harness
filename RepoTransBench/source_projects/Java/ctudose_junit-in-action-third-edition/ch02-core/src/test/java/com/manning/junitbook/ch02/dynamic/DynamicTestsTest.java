package com.manning.junitbook.ch02.dynamic;

import com.manning.junitbook.ch02.predicate.PositiveNumberPredicate;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;
import org.junit.jupiter.api.function.Executable;

import java.util.Arrays;
import java.util.Collection;
import java.util.Iterator;
import java.util.List;
import java.util.stream.IntStream;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.DynamicTest.dynamicTest;

class DynamicTestsTest {

    @TestFactory
    Collection<DynamicTest> dynamicTestsWithCollection() {
        return Arrays.asList(
                dynamicTest("Add test", () -> assertTrue(true)),
                dynamicTest("Multiply Test", () -> assertTrue(true))
        );
    }

    @TestFactory
    Iterator<DynamicTest> dynamicTestsWithIterator() {
        return Arrays.asList(
                dynamicTest("Add test", () -> assertTrue(true)),
                dynamicTest("Multiply Test", () -> assertTrue(true))
        ).iterator();
    }

    @TestFactory
    Stream<DynamicTest> dynamicTestsWithStream() {
        return Stream.of(
                dynamicTest("Add test", () -> assertTrue(true)),
                dynamicTest("Multiply Test", () -> assertTrue(true))
        );
    }

    @TestFactory
    Stream<DynamicTest> dynamicTestsFromIntStream() {
        // Generates tests for PositiveNumberPredicate
        PositiveNumberPredicate predicate = new PositiveNumberPredicate();
        return IntStream.of(-1, 0, 1)
                .mapToObj(number -> dynamicTest("test" + number, () -> {
                    if (number > 0) {
                        assertTrue(predicate.test(number));
                    } else {
                        assertFalse(predicate.test(number));
                    }
                }));
    }

    @TestFactory
    Stream<DynamicTest> dynamicTestsFromLambda() {
        return Stream.of("foo", "bar", "baz")
                .map(text -> dynamicTest("Test " + text, () -> assertTrue(text.length() > 0)));
    }

    @TestFactory
    Stream<DynamicTest> generateRandomNumberOfTests() {
        return Stream.generate(() -> dynamicTest("Another random test", () -> assertTrue(true)))
                .limit(5);
    }

    @TestFactory
    Stream<DynamicTest> dynamicTestsForPositiveNumberPredicate() {
        PositiveNumberPredicate predicate = new PositiveNumberPredicate();
        List<Integer> numbers = Arrays.asList(1, 0, -1, 5, -3);

        return numbers.stream()
                .map(number -> {
                    String testName = "Test if " + number + " is positive";
                    Executable executable = () -> {
                        if (number > 0) {
                            assertTrue(predicate.test(number));
                        } else {
                            assertFalse(predicate.test(number));
                        }
                    };
                    return dynamicTest(testName, executable);
                });
    }

}
package io.herrmann.generator;

import org.junit.Test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

public class GeneratorPublicTest {
    @Test
    public void testEmptyGenerator() {
        assertEquals(new ArrayList<Object>(), list(new EmptyGenerator()));
    }
    private class EmptyGenerator extends Generator {
        @Override
        protected void run() {
        }
    }
    public static <T> List<T> list(Iterable<T> iterable) {
        List<T> result = new ArrayList<T>();
        for (T item : iterable)
            result.add(item);
        return result;
    }
    @Test
    public void testOneEltGenerator() {
        List<String> oneEltList = Arrays.asList("hello");
        assertEquals(oneEltList, list(new ListGenerator<String>(oneEltList)));
    }
    private class ListGenerator<T> extends Generator<T> {
        private final List<T> elements;
        public ListGenerator(List<T> elements) {
            this.elements = elements;
        }
        protected void run() throws InterruptedException {
            for (T element : elements)
                yield(element);
        }
    }
    @Test
    public void testTwoEltGenerator() {
        List<Double> twoEltList = Arrays.asList(3.14, 2.71);
        assertEquals(twoEltList, list(new ListGenerator<Double>(twoEltList)));
    }
    @Test
    public void testInfiniteGenerator() {
        InfiniteGenerator generator = new InfiniteGenerator();
        testInfiniteGenerator(generator);
    }
    public void testInfiniteGenerator(InfiniteGenerator generator) {
        int NUM_ELTS_TO_INSPECT = 777;
        Iterator<String> generatorIterator = generator.iterator();
        for (int i=0; i < NUM_ELTS_TO_INSPECT; i++) {
            assertTrue(generatorIterator.hasNext());
            assertEquals("repeat", generatorIterator.next());
        }
    }
    private class InfiniteGenerator extends Generator<String> {
        @Override
        protected void run() throws InterruptedException {
            while (true)
                yield("repeat");
        }
    }
    @Test
    public void testInfiniteGeneratorLeavesNoRunningThreads() throws Throwable {
        InfiniteGenerator generator = new InfiniteGenerator();
        testInfiniteGenerator(generator);
        generator.finalize();
        assertEquals(Thread.State.TERMINATED, generator.producer.getState());
    }

    private class CustomRuntimeException extends RuntimeException {}

    private class GeneratorRaisingException extends Generator<String> {
        @Override
        protected void run() throws InterruptedException {
            throw new CustomRuntimeException();
        }
    }

    @Test(expected = CustomRuntimeException.class)
    public void testGeneratorRaisingExceptionHasNext() {
        GeneratorRaisingException generator = new GeneratorRaisingException();
        Iterator<String> iterator = generator.iterator();
        iterator.hasNext();
    }

    @Test(expected = CustomRuntimeException.class)
    public void testGeneratorRaisingExceptionNext() {
        GeneratorRaisingException generator = new GeneratorRaisingException();
        Iterator<String> iterator = generator.iterator();
        iterator.next();
    }

}
package com.example.aiodataloader.original;

import com.example.aiodataloader.Util;
import org.junit.jupiter.api.Test;
import java.util.concurrent.CompletableFuture;
import java.util.function.Function;
import static org.junit.jupiter.api.Assertions.*;

public class DataLoaderAdditionalOriginalTest {
    @Test
    public void testIsCoroutineFunctionOrPartialTrueOnCoroFn() {
        Function<Object, CompletableFuture<Integer>> coroutineFn = k -> CompletableFuture.completedFuture(1);
        assertTrue(Util.isCoroutineFunctionOrPartial(coroutineFn), "Should detect coroutine style function");
    }

    @Test
    public void testIsCoroutineFunctionOrPartialTrueOnPartialCoro() {
        Function<Object, CompletableFuture<Integer>> baseFn = k -> CompletableFuture.completedFuture(1);
        Function<Object, CompletableFuture<Integer>> partialCoro = baseFn;  // In Java, partial is just assignment
        assertTrue(Util.isCoroutineFunctionOrPartial(partialCoro), "Should detect partial coroutine function");
    }

    @Test
    public void testIsCoroutineFunctionOrPartialFalseOnSyncFn() {
        Function<Object, Integer> syncFn = k -> 1;
        assertFalse(Util.isCoroutineFunctionOrPartial(syncFn), "Should not detect sync function as coroutine");
    }

    @Test
    public void testVersion() {
        assertEquals("1.2.3", Util.VERSION);
    }
}
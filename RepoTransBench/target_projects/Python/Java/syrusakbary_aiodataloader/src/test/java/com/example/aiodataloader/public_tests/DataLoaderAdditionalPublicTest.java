package com.example.aiodataloader.public_tests;

import com.example.aiodataloader.Util;
import org.junit.jupiter.api.Test;
import java.util.concurrent.CompletableFuture;
import java.util.function.Function;
import static org.junit.jupiter.api.Assertions.*;

public class DataLoaderAdditionalPublicTest {
    @Test
    public void testIsCoroutineFunctionOrPartialTrueOnCoroFnPublic() {
        Function<Object, CompletableFuture<Integer>> coroutineFn = k -> CompletableFuture.completedFuture(2);
        assertTrue(Util.isCoroutineFunctionOrPartial(coroutineFn), "Should detect coroutine style function");
    }

    @Test
    public void testIsCoroutineFunctionOrPartialTrueOnPartialCoroPublic() {
        Function<Object, CompletableFuture<Integer>> baseFn = k -> CompletableFuture.completedFuture(3);
        Function<Object, CompletableFuture<Integer>> partialCoro = baseFn;
        assertTrue(Util.isCoroutineFunctionOrPartial(partialCoro), "Should detect partial coroutine function");
    }

    @Test
    public void testIsCoroutineFunctionOrPartialFalseOnSyncFnPublic() {
        Function<Object, Integer> syncFn = k -> 2;
        assertFalse(Util.isCoroutineFunctionOrPartial(syncFn), "Should not detect sync function as coroutine");
    }

    @Test
    public void testVersionPublic() {
        assertEquals("1.2.3", Util.VERSION);
    }
}
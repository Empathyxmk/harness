package com.example.aiodataloader.original;

import com.example.aiodataloader.DataLoader;
import com.example.aiodataloader.Util;
import org.junit.jupiter.api.Test;
import java.util.*;
import java.util.concurrent.*;
import java.util.function.Function;
import static org.junit.jupiter.api.Assertions.*;

public class DataLoaderOriginalTest {
    @Test
    public void testBuildASimpleDataLoader() throws Exception {
        DataLoader<Integer, Integer> loader = new DataLoader<>(keys -> {
            List<CompletableFuture<Integer>> results = new ArrayList<>();
            for (Integer k : keys) {
                results.add(CompletableFuture.completedFuture(k + 1));
            }
            return results;
        });

        CompletableFuture<Integer> f = loader.load(1);
        Integer res = f.get(1, TimeUnit.SECONDS);
        assertEquals(2, res);
    }

    @Test
    public void testCanBuildADataLoaderFromAPartial() throws Exception {
        Function<List<Integer>, List<CompletableFuture<Integer>>> batchLoadFn = keys -> {
            List<CompletableFuture<Integer>> results = new ArrayList<>();
            for (Integer k : keys) {
                results.add(CompletableFuture.completedFuture(k * 2));
            }
            return results;
        };
        DataLoader<Integer, Integer> loader = new DataLoader<>(batchLoadFn);

        CompletableFuture<Integer> f = loader.load(10);
        assertEquals(20, f.get(1, TimeUnit.SECONDS));
    }

    @Test
    public void testSupportsLoadingMultipleKeysInOneCall() throws Exception {
        DataLoader<Integer, Integer> loader = new DataLoader<>(keys -> {
            List<CompletableFuture<Integer>> results = new ArrayList<>();
            for (Integer k : keys) {
                results.add(CompletableFuture.completedFuture(k * 2));
            }
            return results;
        });

        CompletableFuture<List<Integer>> future = loader.loadMany(Arrays.asList(1, 2, 3));
        List<Integer> res = future.get(1, TimeUnit.SECONDS);
        assertEquals(Arrays.asList(2, 4, 6), res);
    }
}
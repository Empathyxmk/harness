package com.example.aiodataloader.public_tests;

import com.example.aiodataloader.DataLoader;
import org.junit.jupiter.api.Test;
import java.util.*;
import java.util.concurrent.*;
import java.util.function.Function;
import static org.junit.jupiter.api.Assertions.*;

public class DataLoaderPublicTest {
    @Test
    public void testBuildASimpleDataLoaderPublic() throws Exception {
        DataLoader<Integer, Integer> loader = new DataLoader<>(keys -> {
            List<CompletableFuture<Integer>> results = new ArrayList<>();
            for (Integer k : keys) {
                results.add(CompletableFuture.completedFuture(k + 1));
            }
            return results;
        });

        CompletableFuture<Integer> f = loader.load(5);
        Integer res = f.get(1, TimeUnit.SECONDS);
        assertEquals(6, res);
    }

    @Test
    public void testCanBuildADataLoaderFromAPartialPublic() throws Exception {
        Function<List<Integer>, List<CompletableFuture<Integer>>> batchLoadFn = keys -> {
            List<CompletableFuture<Integer>> results = new ArrayList<>();
            for (Integer k : keys) {
                results.add(CompletableFuture.completedFuture(k * 4));
            }
            return results;
        };
        DataLoader<Integer, Integer> loader = new DataLoader<>(batchLoadFn);
        CompletableFuture<Integer> f = loader.load(3);
        assertEquals(12, f.get(1, TimeUnit.SECONDS));
    }

    @Test
    public void testSupportsLoadingMultipleKeysInOneCallPublic() throws Exception {
        DataLoader<Integer, Integer> loader = new DataLoader<>(keys -> {
            List<CompletableFuture<Integer>> results = new ArrayList<>();
            for (Integer k : keys) {
                results.add(CompletableFuture.completedFuture(k * 3));
            }
            return results;
        });

        CompletableFuture<List<Integer>> future = loader.loadMany(Arrays.asList(1, 2, 3));
        List<Integer> res = future.get(1, TimeUnit.SECONDS);
        assertEquals(Arrays.asList(3, 6, 9), res);
    }
}
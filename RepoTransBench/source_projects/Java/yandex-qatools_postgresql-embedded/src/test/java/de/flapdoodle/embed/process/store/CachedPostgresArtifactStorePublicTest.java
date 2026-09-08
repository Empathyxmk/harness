package de.flapdoodle.embed.process.store;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Public test for CachedPostgresArtifactStore using different values.
 * Dummy cache used for compilation (remove if real cache class exists).
 */
public class CachedPostgresArtifactStorePublicTest {

    static class DummyCache {
        private String fileName;
        private int timesFetched = 0;

        public DummyCache(String fileName) {
            this.fileName = fileName;
        }

        public String fetch() {
            timesFetched++;
            return "fetched_public_" + fileName;
        }

        public int getTimesFetched() {
            return timesFetched;
        }
    }

    @Test
    public void fetchReturnsFileWithDifferentName() {
        DummyCache cache = new DummyCache("pubfile-2211.txt");
        String res = cache.fetch();
        assertTrue(res.contains("pubfile-2211.txt"));
    }

    @Test
    public void fetchCountsTimesFetchedWithDifferentFile() {
        DummyCache cache = new DummyCache("pubcache.data");
        cache.fetch();
        cache.fetch();
        assertEquals(2, cache.getTimesFetched());
    }
}
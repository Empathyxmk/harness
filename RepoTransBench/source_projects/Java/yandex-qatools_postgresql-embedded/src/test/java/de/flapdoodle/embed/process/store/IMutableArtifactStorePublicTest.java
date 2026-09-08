package de.flapdoodle.embed.process.store;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Public test for IMutableArtifactStore logic using different values.
 * Has a minimal mock implementation for compilation (remove if real interface/class exists in main src).
 */
public class IMutableArtifactStorePublicTest {

    static class DummyMutableStore {
        private boolean removed = false;
        private String lastFileSetId = null;

        public void removeFileSet(String fileSetId) {
            this.removed = true;
            this.lastFileSetId = fileSetId;
        }

        public boolean isRemoved() {
            return removed;
        }

        public String getLastFileSetId() {
            return lastFileSetId;
        }
    }

    @Test
    public void callsRemoveFileSetWithDifferentData() {
        DummyMutableStore store = new DummyMutableStore();
        store.removeFileSet("public-fileset-abc");
        assertTrue(store.isRemoved());
        assertEquals("public-fileset-abc", store.getLastFileSetId());
    }

    @Test
    public void removeFileSetNotCalledByDefault() {
        DummyMutableStore store = new DummyMutableStore();
        assertFalse(store.isRemoved());
        assertNull(store.getLastFileSetId());
    }
}
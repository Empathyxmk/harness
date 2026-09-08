package de.flapdoodle.embed.process.store;

import de.flapdoodle.embed.process.config.store.IDownloadConfig;
import org.junit.Test;

import static org.junit.Assert.*;

public class IMutableArtifactStoreTest {
    private static class TestMutableArtifactStore implements IMutableArtifactStore {
        public boolean configSet = false;
        @Override public void setDownloadConfig(IDownloadConfig downloadConfig) { configSet = true; }
        @Override public void removeFileSet(Object d, Object fs) {}
        @Override public boolean checkDistribution(Object d) {return false;}
        @Override public Object extractFileSet(Object d) {return null;}
    }

    @Test
    public void testSetDownloadConfig() {
        TestMutableArtifactStore store = new TestMutableArtifactStore();
        assertFalse(store.configSet);
        store.setDownloadConfig(null);
        assertTrue(store.configSet);
    }
}
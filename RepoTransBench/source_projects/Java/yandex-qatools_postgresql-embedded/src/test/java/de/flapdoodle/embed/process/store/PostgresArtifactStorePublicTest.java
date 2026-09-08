package de.flapdoodle.embed.process.store;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Public test for PostgresArtifactStore using alternative values.
 * Dummy class here for isolation (remove if real class exists in main src).
 */
public class PostgresArtifactStorePublicTest {

    static class PostgresArtifactStoreFake {
        private String artifact;

        public PostgresArtifactStoreFake(String artifact) {
            this.artifact = artifact;
        }

        public String getArtifact() {
            return artifact;
        }

        public void setArtifact(String artifact) {
            this.artifact = artifact;
        }
    }

    @Test
    public void storesArtifactNameWithDifferentValue() {
        PostgresArtifactStoreFake store = new PostgresArtifactStoreFake("public-art-unique-192");
        assertEquals("public-art-unique-192", store.getArtifact());
    }

    @Test
    public void setArtifactUpdatesArtifactWithAnotherValue() {
        PostgresArtifactStoreFake store = new PostgresArtifactStoreFake("start-art-public-1");
        store.setArtifact("set-artifact-public-2");
        assertEquals("set-artifact-public-2", store.getArtifact());
    }
}
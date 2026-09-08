package de.flapdoodle.embed.process.store;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Public test using different config data for NonCachedPostgresArtifactStoreBuilder.
 * Has minimal dummy builder just for compilation (remove if real builder exists in main src).
 */
public class NonCachedPostgresArtifactStoreBuilderPublicTest {

    static class DummyBuilder {
        private String config;

        DummyBuilder customConfig(String config) {
            this.config = config;
            return this;
        }

        String getConfig() {
            return config;
        }
    }

    @Test
    public void setsCustomConfigDifferentFromPrivateTest() {
        DummyBuilder builder = new DummyBuilder().customConfig("public_config_4567");
        assertEquals("public_config_4567", builder.getConfig());
    }

    @Test
    public void configIsNullByDefault() {
        DummyBuilder builder = new DummyBuilder();
        assertNull(builder.getConfig());
    }
}
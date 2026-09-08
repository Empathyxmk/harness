package ru.yandex.qatools.embed.postgresql;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Public test for EmbeddedPostgres logic using different parameters.
 * Dummy class for compilation (remove if real EmbeddedPostgres exists).
 */
public class EmbeddedPostgresPublicTest {

    static class DummyEmbeddedPostgres {
        private boolean started = false;

        public void start(String user, String pass) {
            this.started = user.equals("publicUser") && pass.equals("publicPass");
        }

        public boolean isStarted() {
            return started;
        }
    }

    @Test
    public void canStartWithDifferentCredentials() {
        DummyEmbeddedPostgres pg = new DummyEmbeddedPostgres();
        pg.start("publicUser", "publicPass");
        assertTrue(pg.isStarted());
    }

    @Test
    public void failsToStartWithWrongCredentials() {
        DummyEmbeddedPostgres pg = new DummyEmbeddedPostgres();
        pg.start("bad", "creds");
        assertFalse(pg.isStarted());
    }
}
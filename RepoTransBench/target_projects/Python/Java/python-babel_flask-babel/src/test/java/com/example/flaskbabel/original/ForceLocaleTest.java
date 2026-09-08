package com.example.flaskbabel.original;

import org.junit.jupiter.api.Test;

import java.util.concurrent.Semaphore;

import static org.junit.jupiter.api.Assertions.*;

class ForceLocaleTest {

    @Test
    void testForceLocale() {
        DummyFlaskApp app = new DummyFlaskApp();
        Babel b = new Babel(app, () -> "de_DE");

        try (DummyRequestContext ctx = app.testRequestContext()) {
            assertEquals("de_DE", b.getLocale().toString());
            try (ForceLocaleContext ignored = b.forceLocale("en_US")) {
                assertEquals("en_US", b.getLocale().toString());
            }
            assertEquals("de_DE", b.getLocale().toString());
        }
    }

    @Test
    void testForceLocaleWithThreading() throws InterruptedException {
        DummyFlaskApp app = new DummyFlaskApp();
        Babel b = new Babel(app, () -> "de_DE");
        Semaphore semaphore = new Semaphore(0);

        Thread thread = new Thread(() -> {
            try (DummyRequestContext ctx = app.testRequestContext()) {
                try (ForceLocaleContext ignored = b.forceLocale("en_US")) {
                    assertEquals("en_US", b.getLocale().toString());
                    semaphore.acquire();
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
            }
        });
        thread.start();

        try (DummyRequestContext ctx = app.testRequestContext()) {
            assertEquals("de_DE", b.getLocale().toString());
        } finally {
            semaphore.release();
            thread.join();
        }
    }

    @Test
    void testForceLocaleWithThreadingAndAppContext() throws InterruptedException {
        DummyFlaskApp app = new DummyFlaskApp();
        Babel b = new Babel(app, () -> "de_DE");
        Semaphore semaphore = new Semaphore(0);

        Thread thread = new Thread(() -> {
            try (DummyAppContext ctx = app.appContext()) {
                try (ForceLocaleContext ignored = b.forceLocale("en_US")) {
                    assertEquals("en_US", b.getLocale().toString());
                    semaphore.acquire();
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
            }
        });
        thread.start();

        try (DummyAppContext ctx = app.appContext()) {
            assertEquals("de_DE", b.getLocale().toString());
        } finally {
            semaphore.release();
            thread.join();
        }
    }

    @Test
    void testRefreshDuringForceLocale() {
        DummyFlaskApp app = new DummyFlaskApp();
        Babel b = new Babel(app, () -> "de_DE");
        try (DummyRequestContext ctx = app.testRequestContext()) {
            try (ForceLocaleContext ignored = b.forceLocale("en_US")) {
                assertEquals("en_US", b.getLocale().toString());
                b.refresh();
                assertEquals("en_US", b.getLocale().toString());
            }
        }
    }
}
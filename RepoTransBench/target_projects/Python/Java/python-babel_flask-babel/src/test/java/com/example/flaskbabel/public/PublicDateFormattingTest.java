package com.example.flaskbabel.public;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.time.*;

class PublicDateFormattingTest {

    @Test
    void testPublicFormatTime() {
        DummyFlaskApp app = new DummyFlaskApp();
        Babel b = new Babel(app);
        LocalDateTime dt = LocalDateTime.of(2021, 8, 14, 22, 15, 30);
        try (DummyRequestContext ctx = app.testRequestContext()) {
            String s = b.formatTime(dt, "short");
            assertNotNull(s);
            assertTrue(s.chars().anyMatch(Character::isDigit));
        }
    }

    @Test
    void testPublicFormatDate() {
        DummyFlaskApp app = new DummyFlaskApp();
        Babel b = new Babel(app);
        LocalDateTime d = LocalDateTime.of(2022, 7, 20, 0, 0, 0);
        try (DummyRequestContext ctx = app.testRequestContext()) {
            String s = b.formatDate(d, "long");
            assertNotNull(s);
            assertTrue(s.contains("2022") || s.contains("20"));
        }
    }

    @Test
    void testPublicFormatDatetime() {
        DummyFlaskApp app = new DummyFlaskApp();
        Babel b = new Babel(app);
        LocalDateTime d = LocalDateTime.of(2020, 12, 31, 19, 45, 16);
        try (DummyRequestContext ctx = app.testRequestContext()) {
            String s = b.formatDatetime(d, "full");
            assertNotNull(s);
            assertTrue((s.contains("2020") || s.contains("31")) && s.contains(":"));
        }
    }

    @Test
    void testPublicFormatTimedelta() {
        DummyFlaskApp app = new DummyFlaskApp();
        Babel b = new Babel(app);
        Duration delta = Duration.ofDays(3).plusHours(1).plusMinutes(25);
        try (DummyRequestContext ctx = app.testRequestContext()) {
            String s = b.formatTimedelta(delta);
            assertNotNull(s);
            assertTrue(s.contains("3") || s.contains("day"));
        }
    }

    @Test
    void testPublicFormatTimeCustomLocale() {
        DummyFlaskApp app = new DummyFlaskApp();
        Babel b = new Babel(app);
        LocalDateTime dt = LocalDateTime.of(2023, 6, 15, 17, 40, 0);
        try (DummyRequestContext ctx = app.testRequestContext()) {
            String s = b.formatTime(dt, "short", "it");
            assertNotNull(s);
            assertTrue(s.contains(":"));
        }
    }
}
package com.example.flaskbabel.original;

import org.junit.jupiter.api.Test;

import java.time.*;
import java.time.temporal.ChronoUnit;

import static org.junit.jupiter.api.Assertions.*;

class DateFormattingTest {

    @Test
    void testBasics() {
        DummyFlaskApp app = new DummyFlaskApp();
        Babel b = new Babel(app);

        LocalDateTime d = LocalDateTime.of(2010, 4, 12, 13, 46, 0);
        Duration delta = Duration.ofDays(6);

        try (DummyRequestContext ctx1 = app.testRequestContext()) {
            assertEquals("Apr 12, 2010, 1:46:00 PM", b.formatDatetime(d));
            assertEquals("Apr 12, 2010", b.formatDate(d));
            assertEquals("1:46:00 PM", b.formatTime(d));
            assertEquals("1 week", b.formatTimedelta(delta));
            assertEquals("6 days", b.formatTimedelta(delta, 1));
        }

        try (DummyRequestContext ctx2 = app.testRequestContext()) {
            b.setDefaultTimezone("Europe/Vienna");
            assertEquals("Apr 12, 2010, 3:46:00 PM", b.formatDatetime(d));
            assertEquals("Apr 12, 2010", b.formatDate(d));
            assertEquals("3:46:00 PM", b.formatTime(d));
        }

        try (DummyRequestContext ctx3 = app.testRequestContext()) {
            b.setDefaultLocale("de_DE");
            assertEquals("12. April 2010, 15:46:00 MESZ", b.formatDatetime(d, "long"));
        }
    }

    @Test
    void testCustomFormats() {
        DummyFlaskApp app = new DummyFlaskApp();
        app.setConfig("BABEL_DEFAULT_LOCALE", "en_US");
        app.setConfig("BABEL_DEFAULT_TIMEZONE", "Pacific/Johnston");
        Babel b = new Babel(app);
        b.setDateFormat("datetime", "long");
        b.setDateFormat("datetime.long", "MMMM d, yyyy h:mm:ss a");
        LocalDateTime d = LocalDateTime.of(2010, 4, 12, 13, 46, 0);

        try (DummyRequestContext ctx = app.testRequestContext()) {
            assertEquals("April 12, 2010 3:46:00 AM", b.formatDatetime(d));
        }
    }

    @Test
    void testCustomLocaleSelector() {
        DummyFlaskApp app = new DummyFlaskApp();
        Babel b = new Babel(app);
        LocalDateTime d = LocalDateTime.of(2010, 4, 12, 13, 46, 0);

        // Mutable containers to act like Python's nonlocal vars
        final String[] theLocale = {"en_US"};
        final String[] theTimezone = {"UTC"};

        b.setLocaleSelector(() -> theLocale[0]);
        b.setTimezoneSelector(() -> theTimezone[0]);

        try (DummyRequestContext ctx = app.testRequestContext()) {
            assertEquals("Apr 12, 2010, 1:46:00 PM", b.formatDatetime(d));
        }

        theLocale[0] = "de_DE";
        theTimezone[0] = "Europe/Vienna";
        try (DummyRequestContext ctx2 = app.testRequestContext()) {
            assertEquals("12.04.2010, 15:46:00", b.formatDatetime(d));
        }
    }

    @Test
    void testRefreshing() {
        DummyFlaskApp app = new DummyFlaskApp();
        Babel b = new Babel(app);
        LocalDateTime d = LocalDateTime.of(2010, 4, 12, 13, 46, 0);
        try (DummyRequestContext ctx = app.testRequestContext()) {
            assertEquals("Apr 12, 2010, 1:46:00 PM", b.formatDatetime(d));
            b.setDefaultTimezone("Europe/Vienna");
            b.refresh();
            assertEquals("Apr 12, 2010, 3:46:00 PM", b.formatDatetime(d));
        }
    }
}
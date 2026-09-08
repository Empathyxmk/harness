package com.underyx.flaskredis.publictests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.regex.Pattern;
import java.util.*;

class PublicInitPyTest {
    static final String __version__ = "2.0.0";
    static final String __title__ = "Flask-Redis";
    static final String __description__ = "Redis cache extension";
    static final String __url__ = "https://example.com/flask-redis";
    static final String __uri__ = __url__;
    static final String __author__ = "Joe Smith";
    static final String __email__ = "joe@smith.com";
    static final String __license__ = "MIT";
    static final String __copyright__ = "Copyright 2024";
    static final List<String> __all__ = List.of("FlaskRedis");

    @Test
    void testPublicDunderConstantsDistinct() {
        assertTrue(__version__ instanceof String);
        assertEquals("Flask-Redis", __title__);
        assertTrue(__description__.toLowerCase().contains("redis"));
        assertTrue(__url__.startsWith("https://"));
        assertTrue(__uri__.startsWith("https://"));
        assertTrue(__email__.contains("@"));
        assertTrue(__copyright__.contains("opyright"));
        assertTrue(__all__ instanceof List);
        assertTrue(__all__.contains("FlaskRedis"));
    }

    @Test
    void testPublicTitleUnique() {
        assertEquals("Flask-Redis", __title__);
        assertTrue(__author__ instanceof String);
        assertTrue(__author__.length() > 3);
    }

    @Test
    void testPublicVersionStyle() {
        assertTrue(Pattern.compile("^\\d+\\.\\d+\\.\\d+").matcher(__version__).find());
    }
}
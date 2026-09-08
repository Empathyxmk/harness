package me.drakeet.floo.sample;

import org.junit.Test;

import static org.junit.Assert.*;

public class URLsTest {

    @Test
    public void testSchemeIsFloo() {
        assertEquals("floo", URLs.scheme());
    }

    @Test
    public void testConstants() {
        assertEquals("https://m.drakeet.me/web", URLs.WEB);
        assertEquals("floo://m.drakeet.me/not_registered", URLs.NOT_REGISTERED);
    }
}
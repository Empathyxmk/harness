package com.vimalloc.flaskjwt.publictests;

import org.junit.jupiter.api.Test;

public class PublicViewDecoratorsTest {
    @Test
    public void testPublicDecoratorDummy() {
        assertEquals("FOO", "foo".toUpperCase());
    }
}
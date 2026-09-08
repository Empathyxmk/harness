package com.hankkin.library;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Public test for MyImageLoader singleton pattern
 */
public class MyImageLoaderPublicTest {
    @Test
    public void publicSingletonInstanceDifferentCallNotNull() {
        MyImageLoader instanceA = MyImageLoader.getInstance();
        MyImageLoader instanceB = MyImageLoader.getInstance();
        assertNotNull(instanceA);
        assertNotNull(instanceB);
        assertSame(instanceA, instanceB);
    }
}
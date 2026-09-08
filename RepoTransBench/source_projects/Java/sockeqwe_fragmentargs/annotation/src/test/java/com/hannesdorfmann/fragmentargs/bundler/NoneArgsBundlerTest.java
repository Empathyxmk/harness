package com.hannesdorfmann.fragmentargs.bundler;

import org.junit.Test;
import android.os.Bundle;

import static org.junit.Assert.*;

public class NoneArgsBundlerTest {

    @Test
    public void testGetInstanceReturnsSingleton() {
        NoneArgsBundler a = NoneArgsBundler.get();
        NoneArgsBundler b = NoneArgsBundler.get();
        assertSame("get() should always return same instance", a, b);
    }

    @Test
    public void testPutReturnsNull() {
        assertNull("put should always return null", NoneArgsBundler.get().put("key", 123, new Bundle()));
    }

    @Test
    public void testGetReturnsNull() {
        assertNull("get should always return null", NoneArgsBundler.get().get("key", new Bundle()));
    }
}
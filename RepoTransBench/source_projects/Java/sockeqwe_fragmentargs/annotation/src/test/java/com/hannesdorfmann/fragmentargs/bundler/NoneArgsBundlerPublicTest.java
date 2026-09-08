package com.hannesdorfmann.fragmentargs.bundler;

import org.junit.Test;
import android.os.Bundle;

import static org.junit.Assert.*;

public class NoneArgsBundlerPublicTest {

    @Test
    public void publicTestInstanceSingleton() {
        NoneArgsBundler a = NoneArgsBundler.get();
        NoneArgsBundler b = NoneArgsBundler.get();
        assertTrue("get() should be same instance", a == b);
    }

    @Test
    public void publicTestPutNullAlways() {
        assertNull("Should always return null from put", NoneArgsBundler.get().put("publicKey", "hello", new Bundle()));
    }

    @Test
    public void publicTestGetNullAlways() {
        assertNull("Should always return null from get", NoneArgsBundler.get().get("anotherKey", new Bundle()));
    }
}
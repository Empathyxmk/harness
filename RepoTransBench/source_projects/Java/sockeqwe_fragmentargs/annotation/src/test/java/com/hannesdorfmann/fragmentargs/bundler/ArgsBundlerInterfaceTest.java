package com.hannesdorfmann.fragmentargs.bundler;

import org.junit.Test;
import android.os.Bundle;

public class ArgsBundlerInterfaceTest {

    static class StringArgsBundler implements ArgsBundler<String> {
        @Override
        public void put(String key, String value, Bundle bundle) {
            bundle.putParcelableArrayList(key, null); // just exercising the interface
        }

        @Override
        public <V extends String> V get(String key, Bundle bundle) {
            return null;
        }
    }

    @Test
    public void testCustomImplementation() {
        StringArgsBundler bundler = new StringArgsBundler();
        bundler.put("foo", "bar", new Bundle());
        bundler.get("foo", new Bundle());
    }
}
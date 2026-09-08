package com.hannesdorfmann.fragmentargs.bundler;

import android.os.Bundle;
import org.junit.Test;

import static org.junit.Assert.*;

public class ArgsBundlerInterfacePublicTest {

    static class PublicTestBundler extends ArgsBundler<String> {
        @Override
        public void put(String key, String value, Bundle bundle) {
            bundle.putString(key, "PUBLIC_" + value + "_PUBTEST");
        }

        @Override
        public String get(String key, Bundle bundle) {
            String v = bundle.getString(key);
            return (v == null) ? null : v.replace("PUBLIC_", "").replace("_PUBTEST", "");
        }
    }

    @Test
    public void interfacePutAddsPrefixSuffix_Public() {
        Bundle bundle = new Bundle();
        new PublicTestBundler().put("PUBKEY", "valueForPublic", bundle);
        assertEquals("PUBLIC_valueForPublic_PUBTEST", bundle.getString("PUBKEY"));
    }

    @Test
    public void interfaceGetRemovesPrefixSuffix_Public() {
        Bundle bundle = new Bundle();
        bundle.putString("PUB_KEY", "PUBLIC_zxy_PUBTEST");
        assertEquals("zxy", new PublicTestBundler().get("PUB_KEY", bundle));
    }
}
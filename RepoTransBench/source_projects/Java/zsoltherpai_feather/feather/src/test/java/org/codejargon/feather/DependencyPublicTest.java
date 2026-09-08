package org.codejargon.feather;

import org.junit.Test;

import javax.inject.Provider;

import static org.junit.Assert.assertNotNull;

public class DependencyPublicTest {
    @Test
    public void dependencyInstance_public() {
        Feather feather = Feather.with();
        assertNotNull(feather.instance(PublicPlain.class));
    }

    @Test
    public void provider_public() {
        Feather feather = Feather.with();
        Provider<PublicPlain> plainProvider = feather.provider(PublicPlain.class);
        assertNotNull(plainProvider.get());
    }

    @Test(expected = FeatherException.class)
    public void unknown_public() {
        Feather feather = Feather.with();
        feather.instance(AnotherUnknown.class);
    }

    public static class PublicPlain {

    }

    public static class AnotherUnknown {
        public AnotherUnknown(int diffConstructor) {

        }
    }
}
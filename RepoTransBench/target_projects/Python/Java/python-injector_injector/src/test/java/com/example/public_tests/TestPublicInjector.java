package com.example.public_tests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TestPublicInjector {

    // Simulated equivalents for Python's injector classes

    interface Provider<T> {
        T get();
    }

    static class InstanceProvider<T> implements Provider<T> {
        private final T instance;
        public InstanceProvider(T instance) {
            this.instance = instance;
        }
        @Override
        public T get() {
            return instance;
        }
    }

    static class Injector {
        private final java.util.Map<Class<?>, Provider<?>> providers = new java.util.HashMap<>();

        public Injector() {}

        public Injector(Provider<?>[] providerArr) {
            for (Provider<?> p : providerArr) {
                if (p instanceof InstanceProvider<?>) {
                    InstanceProvider<?> ip = (InstanceProvider<?>) p;
                    providers.put(ip.instance.getClass(), ip);
                }
            }
        }

        public <T> T get(Class<T> cls) {
            Provider<?> p = providers.get(cls);
            if (p != null) {
                return cls.cast(p.get());
            }
            throw new RuntimeException("No provider for " + cls);
        }

        public <T> T callWithInjection(java.util.function.Function<Integer, T> fn, int value) {
            return fn.apply(value);
        }
    }

    static class Alpha {}
    static class Beta {}

    @Test
    void testPublicSingletonBindingUniqueValue() {
        Alpha a = new Alpha();
        Beta b = new Beta();
        InstanceProvider<Alpha> alphaProvider = new InstanceProvider<>(a);
        InstanceProvider<Beta> betaProvider = new InstanceProvider<>(b);
        Injector inj = new Injector(new Provider[]{alphaProvider, betaProvider});
        Alpha a1 = inj.get(Alpha.class);
        Beta b1 = inj.get(Beta.class);
        assertNotNull(a1);
        assertNotNull(b1);
        assertSame(a, inj.get(Alpha.class));
        assertSame(b, inj.get(Beta.class));
    }

    @Test
    void testPublicInjectDecoratorWithPrimitive() {
        // Simulate injector.call_with_injection behavior
        Injector inj = new Injector();
        int injectedValue = 77;
        java.util.function.Function<Integer, Integer> provide = (Integer value) -> value;
        int result = inj.callWithInjection(provide, injectedValue);
        assertEquals(77, result);
    }

    @Test
    void testPublicProviderReuseTypes() {
        class Foo {}
        Foo fooInstance = new Foo();
        InstanceProvider<Foo> fooProvider = new InstanceProvider<>(fooInstance);
        Injector inj = new Injector(new Provider[]{fooProvider});
        Foo foo1 = inj.get(Foo.class);
        Foo foo2 = inj.get(Foo.class);
        assertSame(foo1, foo2);
    }
}
package org.caoym.jjvm;

import org.caoym.jjvm.lang.JvmClass;
import org.caoym.jjvm.lang.JvmMethod;
import org.junit.jupiter.api.Test;

import java.nio.file.Path;
import java.nio.file.Paths;

import static org.junit.jupiter.api.Assertions.*;

class VirtualMachineTest {
    static class DummyMethod implements JvmMethod {
        boolean called = false;
        @Override
        public void call(org.caoym.jjvm.runtime.Env env, Object thiz, Object... args) {
            called = true;
        }
        @Override
        public int getParameterCount() { return 1; }
        @Override
        public String getName() { return "main"; }
    }

    static class DummyClass extends JvmClass {
        DummyMethod method = new DummyMethod();

        public DummyClass() {
            super(null, null, null, null, null, null, null, null, false);
        }

        @Override
        public JvmMethod getMethod(String name, String descriptor) {
            if ("main".equals(name) && "([Ljava/lang/String;)V".equals(descriptor)) {
                return method;
            }
            return null;
        }
    }

    static class DummyClassLoader implements org.caoym.jjvm.lang.JvmClassLoader {
        boolean loaded = false;
        @Override
        public JvmClass loadClass(String className) {
            loaded = true;
            return new DummyClass();
        }
    }

    @Test
    void testGetClass_CachesAndReturns() throws Exception {
        VirtualMachine vm = new VirtualMachine(Paths.get("."), "FakeClass");
        // Hack in dummy loader
        java.lang.reflect.Field f = VirtualMachine.class.getDeclaredField("classLoader");
        f.setAccessible(true);
        DummyClassLoader loader = new DummyClassLoader();
        f.set(vm, loader);

        JvmClass cls1 = vm.getClass("hello.FakeClass");
        assertTrue(loader.loaded);
        loader.loaded = false;

        // Should fetch from cache
        JvmClass cls2 = vm.getClass("hello.FakeClass");
        assertFalse(loader.loaded);
        assertSame(cls1, cls2);
    }
}
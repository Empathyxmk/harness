package org.caoym.jjvm;

import org.caoym.jjvm.lang.JvmClass;
import org.caoym.jjvm.lang.JvmClassLoader;
import org.caoym.jjvm.natives.JvmNativeClass;
import org.junit.jupiter.api.Test;

import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.*;

class JvmDefaultClassLoaderTest {
    static class DummyNativeClass extends JvmNativeClass {
        public DummyNativeClass(JvmClassLoader loader, Class<?> hostClass) {
            super(loader, hostClass);
        }
    }

    @Test
    void testNonExistingClassLoadsAsNative() throws Exception {
        // should never find a .class file with this name, so will hit native branch
        // fallback to load a java class in this JVM as a native class
        JvmDefaultClassLoader loader = new JvmDefaultClassLoader(Path.of("."));
        // Use a well-known class present in this JVM
        JvmClass c = loader.loadClass("java.lang.String");
        assertNotNull(c);
        assertTrue(c instanceof JvmNativeClass);
    }

    @Test
    void testConstructorAndClassPath() {
        Path fakePath = Path.of("/tmp");
        JvmDefaultClassLoader loader = new JvmDefaultClassLoader(fakePath);
        assertNotNull(loader);
    }
}
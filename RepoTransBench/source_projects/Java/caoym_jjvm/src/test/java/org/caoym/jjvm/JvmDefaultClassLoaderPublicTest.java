package org.caoym.jjvm;

import org.junit.Test;

import java.io.IOException;

import static org.junit.Assert.*;

public class JvmDefaultClassLoaderPublicTest {

    @Test
    public void testLoadResourceFileWithDifferentResource() throws IOException {
        JvmDefaultClassLoader loader = new JvmDefaultClassLoader();
        // Try some known resource name likely missed in private test
        assertNull(loader.getResourceAsStream("META-INF/not-a-real-resource.txt"));
    }

    @Test
    public void testNonExistingClassReturnsNull() throws IOException {
        JvmDefaultClassLoader loader = new JvmDefaultClassLoader();
        assertNull(loader.loadClassBytes("com/example/NoSuchClass.class"));
    }
}
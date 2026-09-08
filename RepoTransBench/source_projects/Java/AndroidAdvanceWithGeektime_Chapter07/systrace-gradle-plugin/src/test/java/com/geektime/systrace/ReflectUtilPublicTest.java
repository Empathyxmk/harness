package com.geektime.systrace;

import org.junit.Test;

import static org.junit.Assert.*;

import java.lang.reflect.Field;
import java.lang.reflect.Method;

public class ReflectUtilPublicTest {

    static class RootClass {
        private int rootPrivate = 88;
        private int onlyRoot = 202;
        private String rootField = "baz";
        public String rootPublic = "yo";
        public void rootMethod() {}
        private void onlyRootMethod() {}
    }

    static class DerivedClass extends RootClass {
        private int derivedPrivate = 99;
        private String derivedField = "qux";
        public void quxMethod() {}
        private void mystery() {}
    }

    @Test
    public void testGetDeclaredFieldRecursiveOwnClassPublic() throws Exception {
        Field f = ReflectUtil.getDeclaredFieldRecursive(DerivedClass.class, "derivedPrivate");
        assertNotNull(f);
        DerivedClass obj = new DerivedClass();
        f.setAccessible(true);
        assertEquals(99, f.getInt(obj));
    }

    @Test
    public void testGetDeclaredFieldRecursiveSuperClassPublic() throws Exception {
        Field f = ReflectUtil.getDeclaredFieldRecursive(DerivedClass.class, "rootPrivate");
        assertNotNull(f);
        DerivedClass obj = new DerivedClass();
        f.setAccessible(true);
        assertEquals(88, f.getInt(obj));
    }

    @Test(expected = NoSuchFieldException.class)
    public void testGetDeclaredFieldRecursiveNotFoundPublic() throws Exception {
        ReflectUtil.getDeclaredFieldRecursive(DerivedClass.class, "noSuchField");
    }

    @Test(expected = IllegalArgumentException.class)
    public void testGetDeclaredFieldRecursiveBadTypePublic() throws Exception {
        ReflectUtil.getDeclaredFieldRecursive(new Object(), "derivedPrivate");
    }

    @Test
    public void testGetDeclaredFieldRecursiveClassNameStringPublic() throws Exception {
        Field f = ReflectUtil.getDeclaredFieldRecursive("com.geektime.systrace.ReflectUtilPublicTest$DerivedClass", "derivedPrivate");
        assertNotNull(f);
        DerivedClass obj = new DerivedClass();
        f.setAccessible(true);
        assertEquals(99, f.getInt(obj));
    }

    @Test
    public void testGetDeclaredMethodRecursiveOwnClassPublic() throws Exception {
        Method m = ReflectUtil.getDeclaredMethodRecursive(DerivedClass.class, "mystery");
        assertNotNull(m);
    }

    @Test
    public void testGetDeclaredMethodRecursiveSuperClassPublic() throws Exception {
        Method m = ReflectUtil.getDeclaredMethodRecursive(DerivedClass.class, "onlyRootMethod");
        assertNotNull(m);
    }

    @Test(expected = NoSuchMethodException.class)
    public void testGetDeclaredMethodRecursiveNotFoundPublic() throws Exception {
        ReflectUtil.getDeclaredMethodRecursive(DerivedClass.class, "notFoundPublicMethod");
    }

    @Test(expected = IllegalArgumentException.class)
    public void testGetDeclaredMethodRecursiveBadTypePublic() throws Exception {
        ReflectUtil.getDeclaredMethodRecursive(true, "mystery");
    }

    @Test
    public void testGetDeclaredMethodRecursiveClassNameStringPublic() throws Exception {
        Method m = ReflectUtil.getDeclaredMethodRecursive("com.geektime.systrace.ReflectUtilPublicTest$DerivedClass", "mystery");
        assertNotNull(m);
    }

    @Test(expected = UnsupportedOperationException.class)
    public void testPrivateConstructorPublic() {
        new ReflectUtil();
    }
}
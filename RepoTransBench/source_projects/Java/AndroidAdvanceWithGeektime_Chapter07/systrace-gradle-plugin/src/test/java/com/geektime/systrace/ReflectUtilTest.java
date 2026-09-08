package com.geektime.systrace;

import org.junit.Test;

import static org.junit.Assert.*;

import java.lang.reflect.Field;
import java.lang.reflect.Method;

public class ReflectUtilTest {

    static class SuperClass {
        private int superPrivate = 44;
        private int onlySuper = 101;
        private String field = "foo";
        public String superPublic = "hey";
        public void superMethod() {}
        private void onlySuperMethod() {}
    }

    static class SubClass extends SuperClass {
        private int subPrivate = 55;
        private String subField = "bar";
        public void bar() {}
        private void secret() {}
    }

    @Test
    public void testGetDeclaredFieldRecursiveOwnClass() throws Exception {
        Field f = ReflectUtil.getDeclaredFieldRecursive(SubClass.class, "subPrivate");
        assertNotNull(f);
        SubClass obj = new SubClass();
        f.setAccessible(true);
        assertEquals(55, f.getInt(obj));
    }

    @Test
    public void testGetDeclaredFieldRecursiveSuperClass() throws Exception {
        Field f = ReflectUtil.getDeclaredFieldRecursive(SubClass.class, "superPrivate");
        assertNotNull(f);
        SubClass obj = new SubClass();
        f.setAccessible(true);
        assertEquals(44, f.getInt(obj));
    }

    @Test(expected = NoSuchFieldException.class)
    public void testGetDeclaredFieldRecursiveNotFound() throws Exception {
        ReflectUtil.getDeclaredFieldRecursive(SubClass.class, "nonexistent");
    }

    @Test(expected = IllegalArgumentException.class)
    public void testGetDeclaredFieldRecursiveBadType() throws Exception {
        ReflectUtil.getDeclaredFieldRecursive(1234, "subPrivate");
    }

    @Test
    public void testGetDeclaredFieldRecursiveClassNameString() throws Exception {
        Field f = ReflectUtil.getDeclaredFieldRecursive("com.geektime.systrace.ReflectUtilTest$SubClass", "subPrivate");
        assertNotNull(f);
        SubClass obj = new SubClass();
        f.setAccessible(true);
        assertEquals(55, f.getInt(obj));
    }

    @Test
    public void testGetDeclaredMethodRecursiveOwnClass() throws Exception {
        Method m = ReflectUtil.getDeclaredMethodRecursive(SubClass.class, "secret");
        assertNotNull(m);
    }

    @Test
    public void testGetDeclaredMethodRecursiveSuperClass() throws Exception {
        Method m = ReflectUtil.getDeclaredMethodRecursive(SubClass.class, "onlySuperMethod");
        assertNotNull(m);
    }

    @Test(expected = NoSuchMethodException.class)
    public void testGetDeclaredMethodRecursiveNotFound() throws Exception {
        ReflectUtil.getDeclaredMethodRecursive(SubClass.class, "notFoundMethod");
    }

    @Test(expected = IllegalArgumentException.class)
    public void testGetDeclaredMethodRecursiveBadType() throws Exception {
        ReflectUtil.getDeclaredMethodRecursive(5.6, "secret");
    }

    @Test
    public void testGetDeclaredMethodRecursiveClassNameString() throws Exception {
        Method m = ReflectUtil.getDeclaredMethodRecursive("com.geektime.systrace.ReflectUtilTest$SubClass", "secret");
        assertNotNull(m);
    }

    @Test(expected = UnsupportedOperationException.class)
    public void testPrivateConstructor() {
        new ReflectUtil();
    }
}
package de.larma.arthook.xposed;

import org.junit.Test;

import java.lang.reflect.InvocationTargetException;

import static org.junit.Assert.*;

public class UtilsTest {
    public static class DummyMain {
        public static boolean called = false;
        public static Throwable throwable = null;

        public static void main(String[] args) throws Throwable {
            called = true;
            if (throwable != null) throw throwable;
        }
    }

    @Test
    public void testCallMainSuccessful() throws Throwable {
        DummyMain.called = false;
        DummyMain.throwable = null;
        Utils.callMain(DummyMain.class.getName());
        assertTrue(DummyMain.called);
    }

    @Test(expected = Exception.class)
    public void testCallMainThrowsTargetException() throws Throwable {
        DummyMain.called = false;
        DummyMain.throwable = new Exception("test");
        Utils.callMain(DummyMain.class.getName());
    }
}
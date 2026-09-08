package de.larma.arthook.xposed;

import org.junit.Test;

import static org.junit.Assert.*;

public class UtilsPublicTest {
    public static class DummyPublicMain {
        public static boolean called = false;
        public static Throwable throwable = null;

        public static void main(String[] args) throws Throwable {
            called = true;
            if (throwable != null) throw throwable;
        }
    }

    @Test
    public void testCallMainSuccessfulWithDifferentClass() throws Throwable {
        DummyPublicMain.called = false;
        DummyPublicMain.throwable = null;
        Utils.callMain(DummyPublicMain.class.getName());
        assertTrue(DummyPublicMain.called);
    }

    @Test(expected = RuntimeException.class)
    public void testCallMainThrowsTargetRuntimeException() throws Throwable {
        DummyPublicMain.called = false;
        DummyPublicMain.throwable = new RuntimeException("public test");
        Utils.callMain(DummyPublicMain.class.getName());
    }
}
package com.ecmwf.ai_models.original;

import org.junit.jupiter.api.*;
import com.ecmwf.ai_models.main.MainModule;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.security.Permission;

class MainBasicTest {

    static class ExitException extends SecurityException {
        private static final long serialVersionUID = 1L;
        public final int status;
        public ExitException(int status) { this.status = status; }
    }

    static class NoExitSecurityManager extends SecurityManager {
        private final SecurityManager prev;
        private Integer status = null;
        public NoExitSecurityManager(SecurityManager prev) { this.prev = prev; }
        @Override public void checkPermission(Permission perm) {}
        @Override public void checkPermission(Permission perm, Object ctx) {}
        @Override public void checkExit(int status) { throw new ExitException(status); }
        @Override public SecurityManager getSecurityContext() { return prev; }
    }

    @Test
    void test_main_help() {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        PrintStream origOut = System.out;
        SecurityManager origSec = System.getSecurityManager();
        try {
            System.setOut(new PrintStream(baos));
            System.setSecurityManager(new NoExitSecurityManager(origSec));
            Assertions.assertThrows(ExitException.class, () -> {
                MainModule._main(new String[]{"--help"});
            });
            String outStr = baos.toString();
            Assertions.assertTrue(outStr.contains("usage:") || outStr.contains("Usage:"));
        } finally {
            System.setOut(origOut);
            System.setSecurityManager(origSec);
        }
    }

    @Test
    void test_main_models() {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        PrintStream origOut = System.out;
        SecurityManager origSec = System.getSecurityManager();
        try {
            System.setOut(new PrintStream(baos));
            System.setSecurityManager(new NoExitSecurityManager(origSec));
            Assertions.assertThrows(ExitException.class, () -> {
                MainModule._main(new String[]{"--models"});
            });
            String outStr = baos.toString();
            Assertions.assertTrue(outStr.contains("foo") || outStr.contains("bar"));
        } finally {
            System.setOut(origOut);
            System.setSecurityManager(origSec);
        }
    }

    @Test
    void test_main_verbose_debug() {
        // Just ensure it runs with required patches
        MainModule._main(new String[]{"--verbose"});
        // No assertion required, but make sure it does not throw
    }

}
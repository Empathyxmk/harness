package org.caoym.jjvm;

import org.junit.Test;
import static org.junit.Assert.*;

public class JJvmPublicTest {

    @Test
    public void testMainMethodInvocationWithDifferentArgs() {
        String[] args = new String[] { "foo", "bar", "baz" };
        // Just ensure it does not throw, and returns as expected
        JJvm jvm = new JJvm();
        try {
            jvm.main(new String[] { "-version" });
        } catch (Exception e) {
            fail("Should not have thrown exception for '-version'");
        }
    }

    @Test
    public void testCustomArgsToMain() {
        String[] inputArgs = new String[] { "-help" };
        JJvm jvm = new JJvm();
        try {
            jvm.main(inputArgs);
        } catch (Exception e) {
            fail("Should not throw for '-help' argument");
        }
    }
}
package org.cyclopsgroup.jmxterm;

import org.junit.Test;
import javax.management.remote.JMXServiceURL;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

import java.io.IOException;

public class SyntaxUtilsExtraTest {

    static class FakeJavaProcess implements JavaProcess {
        boolean manageable = false;
        boolean startCalled = false;
        @Override public boolean isManageable() { return manageable; }
        @Override public void startManagementAgent() { startCalled = true; manageable = true; }
        @Override public String toUrl() { return "service:jmx:rmi:///jndi/rmi://127.0.0.1:123/jmxrmi"; }
    }

    static class FakeJPM implements JavaProcessManager {
        FakeJavaProcess proc = new FakeJavaProcess();
        boolean returnNull = false;
        boolean returnUnmanageable = false;
        boolean throwOnStart = false;

        @Override
        public JavaProcess get(int pid) {
            if (returnNull) return null;
            proc.manageable = !returnUnmanageable;
            return proc;
        }
    }

    @Test
    public void testGetUrl_pid_manageable() throws IOException {
        FakeJPM jpm = new FakeJPM();
        jpm.proc.manageable = true;
        JMXServiceURL url = SyntaxUtils.getUrl("123", jpm);
        assertNotNull(url);
        assertEquals("service:jmx:rmi:///jndi/rmi://127.0.0.1:123/jmxrmi", url.toString());
    }

    @Test(expected = NullPointerException.class)
    public void testGetUrl_pid_noProcess() throws IOException {
        FakeJPM jpm = new FakeJPM();
        jpm.returnNull = true;
        SyntaxUtils.getUrl("918", jpm);
    }

    @Test
    public void testGetUrl_pid_startManageable() throws IOException {
        FakeJPM jpm = new FakeJPM();
        jpm.returnUnmanageable = true;
        JMXServiceURL url = SyntaxUtils.getUrl("555", jpm);
        assertNotNull(url);
        assertTrue(jpm.proc.startCalled);
        assertEquals("service:jmx:rmi:///jndi/rmi://127.0.0.1:123/jmxrmi", url.toString());
    }

    @Test(expected = IllegalStateException.class)
    public void testGetUrl_pid_failsToBecomeManageable() throws IOException {
        FakeJPM jpm = new FakeJPM();
        jpm.returnUnmanageable = true;
        jpm.proc = new JavaProcess() {
            boolean mgd = false;
            @Override public boolean isManageable() { return mgd; }
            @Override public void startManagementAgent() {/*never sets manageable*/}
            @Override public String toUrl() { return "bad"; }
        };
        SyntaxUtils.getUrl("101", jpm);
    }
}
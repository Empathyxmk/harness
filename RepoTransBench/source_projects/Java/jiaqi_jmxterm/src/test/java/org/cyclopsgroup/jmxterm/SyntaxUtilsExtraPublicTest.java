package org.cyclopsgroup.jmxterm;

import org.junit.Test;
import javax.management.remote.JMXServiceURL;
import static org.junit.Assert.*;

import java.io.IOException;

public class SyntaxUtilsExtraPublicTest {

    static class FakeJavaProcess implements JavaProcess {
        boolean manageable = false;
        boolean startCalled = false;
        @Override public boolean isManageable() { return manageable; }
        @Override public void startManagementAgent() { startCalled = true; manageable = true; }
        @Override public String toUrl() { return "service:jmx:rmi:///jndi/rmi://127.0.0.1:321/jmxrmi"; }
    }

    static class FakeJPM implements JavaProcessManager {
        FakeJavaProcess proc = new FakeJavaProcess();
        boolean returnNull = false;
        boolean returnUnmanageable = false;

        @Override
        public JavaProcess get(int pid) {
            if (returnNull) return null;
            proc.manageable = !returnUnmanageable;
            return proc;
        }
    }

    @Test
    public void testGetUrl_pid_manageable_public() throws IOException {
        FakeJPM jpm = new FakeJPM();
        jpm.proc.manageable = true;
        // Use a new PID string and unique port in the URL
        JMXServiceURL url = SyntaxUtils.getUrl("456", jpm);
        assertNotNull(url);
        assertEquals("service:jmx:rmi:///jndi/rmi://127.0.0.1:321/jmxrmi", url.toString());
    }

    @Test(expected = NullPointerException.class)
    public void testGetUrl_pid_noProcess_public() throws IOException {
        FakeJPM jpm = new FakeJPM();
        jpm.returnNull = true;
        SyntaxUtils.getUrl("888", jpm); // Use a different PID
    }

    @Test
    public void testGetUrl_pid_startManageable_public() throws IOException {
        FakeJPM jpm = new FakeJPM();
        jpm.returnUnmanageable = true;
        // Still expect startManageable logic with new port
        JMXServiceURL url = SyntaxUtils.getUrl("999", jpm);
        assertNotNull(url);
        assertTrue(jpm.proc.startCalled);
        assertEquals("service:jmx:rmi:///jndi/rmi://127.0.0.1:321/jmxrmi", url.toString());
    }

    @Test(expected = IllegalStateException.class)
    public void testGetUrl_pid_failsToBecomeManageable_public() throws IOException {
        FakeJPM jpm = new FakeJPM();
        jpm.returnUnmanageable = true;
        jpm.proc = new JavaProcess() {
            boolean mgd = false;
            @Override public boolean isManageable() { return mgd; }
            @Override public void startManagementAgent() {/*never sets manageable*/}
            @Override public String toUrl() { return "wrong"; }
        };
        SyntaxUtils.getUrl("202", jpm); // Use a new PID
    }
}
package org.cyclopsgroup.jmxterm;

import org.cyclopsgroup.jmxterm.io.*;
import org.junit.Test;

import javax.management.remote.JMXServiceURL;
import java.io.IOException;
import java.util.HashMap;

import static org.junit.Assert.*;

public class SessionPublicTest {
    static class DummySession extends Session {
        private boolean connected = false;
        private boolean disconnected = false;
        private Connection conn;

        DummySession() {
            super(new PrintStreamCommandOutput(System.out), null, new JavaProcessManager() {
                @Override
                public JavaProcess get(int pid) { return null; }
            });
        }

        @Override
        public void connect(JMXServiceURL url, java.util.Map<String, Object> env) throws IOException {
            // Use a different approach: set connected on specific env key
            if (env != null && env.containsKey("secret")) {
                connected = true;
            }
        }
        @Override
        public void disconnect() throws IOException {
            disconnected = true;
        }
        @Override
        public Connection getConnection() {
            return conn;
        }
        @Override
        public boolean isConnected() {
            return connected;
        }
    }

    @Test
    public void testGetDomain_public() {
        DummySession s = new DummySession();
        s.setDomain("anotherDomain");
        assertEquals("anotherDomain", s.getDomain());
    }

    @Test
    public void testBean_public() {
        DummySession s = new DummySession();
        s.setBean("myBeanXX");
        assertEquals("myBeanXX", s.getBean());
    }

    @Test
    public void testClose_public() {
        DummySession s = new DummySession();
        s.close();
        assertTrue(s.isClosed());
    }

    @Test
    public void testIOandConnection_public() throws Exception {
        DummySession s = new DummySession();
        HashMap<String, Object> env = new HashMap<>();
        env.put("secret", "value");
        // Should connect because env has key "secret"
        s.connect(new JMXServiceURL("service:jmx:rmi:///jndi/rmi://example.net:8989/jmxrmi"), env);
        assertTrue(s.isConnected());
        s.disconnect();
    }
}
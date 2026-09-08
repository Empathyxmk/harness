package org.cyclopsgroup.jmxterm;

import org.junit.Test;
import static org.junit.Assert.*;

public class ConnectionPublicTest {

    @Test
    public void testIsClosedInitially() {
        Connection connection = new Connection() {
            private boolean closed = false;
            @Override public boolean isClosed() { return closed; }
            @Override public void close() { closed = true; }
        };
        assertFalse("A new connection should not be closed", connection.isClosed());
        connection.close();
        assertTrue("After closing, connection should be closed", connection.isClosed());
    }

    @Test
    public void testMultipleCloseCalls() {
        Connection connection = new Connection() {
            private boolean closed = false;
            @Override public boolean isClosed() { return closed; }
            @Override public void close() { closed = true; }
        };
        connection.close();
        connection.close();
        assertTrue("Connection should remain closed after multiple closes", connection.isClosed());
    }
}
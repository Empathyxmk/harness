package com.socialwifi.routeros.original;

import com.socialwifi.routeros.base_api.Connection;
import com.socialwifi.routeros.exceptions.RouterOsApiConnectionClosed;
import org.junit.jupiter.api.Test;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class TestSocket {

    static class DummySocket extends Socket {
        private InputStream in;
        private OutputStream out;
        DummySocket(InputStream in, OutputStream out) { this.in = in; this.out = out; }
        public InputStream getInputStream() { return in; }
        public OutputStream getOutputStream() { return out; }
    }

    @Test
    void testConnectionClosesSocket() throws IOException {
        InputStream in = mock(InputStream.class);
        OutputStream out = mock(OutputStream.class);
        Socket s = spy(new DummySocket(in, out));
        doNothing().when(s).close();

        Connection conn = new Connection(s);
        conn.close();
        verify(s, times(1)).close();
    }

    @Test
    void testConnectionReceivesEOF() throws IOException {
        InputStream in = mock(InputStream.class);
        OutputStream out = mock(OutputStream.class);
        Socket s = new DummySocket(in, out);

        when(in.read(any(), eq(0), eq(2))).thenReturn(-1);

        Connection conn = new Connection(s);
        assertThrows(RouterOsApiConnectionClosed.class, () -> conn.receiveData(2));
    }
}
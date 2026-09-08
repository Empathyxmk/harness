package com.socialwifi.routeros.original;

import com.socialwifi.routeros.api_socket.ApiSocket;
import com.socialwifi.routeros.base_api.Connection;
import com.socialwifi.routeros.exceptions.RouterOsApiConnectionClosed;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class TestApiSocket {

    static class DummySocket extends java.net.Socket {
        private InputStream input;
        private OutputStream output;
        DummySocket(InputStream input, OutputStream output) {
            this.input = input;
            this.output = output;
        }
        public InputStream getInputStream() { return input; }
        public OutputStream getOutputStream() { return output; }
    }

    @Test
    void testSendData() throws IOException {
        // Test proper sending of data over socket
        byte[] sendBuffer = new byte[1024];
        OutputStream outputStream = mock(OutputStream.class);
        InputStream inputStream = mock(InputStream.class);

        DummySocket dummySocket = new DummySocket(inputStream, outputStream);
        ApiSocket apiSocket = new ApiSocket(dummySocket);

        byte[] data = {0x10, 0x20, 0x30};
        apiSocket.send(data);

        verify(outputStream, times(1)).write(data);
        verify(outputStream, times(1)).flush();
    }

    @Test
    void testReceiveDataNormal() throws IOException {
        byte[] buffer = {0x01, 0x02};
        InputStream inputStream = mock(InputStream.class);
        OutputStream outputStream = mock(OutputStream.class);
        when(inputStream.read(any(), eq(0), eq(2))).then(invocation -> {
            byte[] arr = invocation.getArgument(0);
            arr[0] = 0x01;
            arr[1] = 0x02;
            return 2;
        });
        DummySocket dummySocket = new DummySocket(inputStream, outputStream);
        ApiSocket apiSocket = new ApiSocket(dummySocket);

        byte[] result = apiSocket.receive(2);
        assertArrayEquals(buffer, result);
    }

    @Test
    void testReceiveDataClosed() throws IOException {
        InputStream inputStream = mock(InputStream.class);
        OutputStream outputStream = mock(OutputStream.class);
        when(inputStream.read(any(), eq(0), eq(2))).thenReturn(-1);

        DummySocket dummySocket = new DummySocket(inputStream, outputStream);
        ApiSocket apiSocket = new ApiSocket(dummySocket);

        assertThrows(RouterOsApiConnectionClosed.class, () -> apiSocket.receive(2));
    }
}
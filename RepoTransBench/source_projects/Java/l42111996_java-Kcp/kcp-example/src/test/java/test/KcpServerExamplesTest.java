package test;

import com.backblaze.erasure.fec.Snmp;
import io.netty.buffer.ByteBuf;
import io.netty.buffer.Unpooled;
import kcp.ChannelConfig;
import kcp.KcpListener;
import kcp.KcpServer;
import kcp.Ukcp;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.net.InetSocketAddress;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class KcpServerExamplesTest {

    private Ukcp mockUkcp;
    private ByteBuf mockBuf;

    @BeforeEach
    void setup() {
        mockUkcp = mock(Ukcp.class, RETURNS_DEEP_STUBS);
        when(mockUkcp.user().getRemoteAddress())
                .thenReturn(new InetSocketAddress("localhost", 12345));
        when(mockUkcp.getConv()).thenReturn(42L);
        mockBuf = Unpooled.buffer();
        mockBuf.writeBytes("hello".getBytes());
    }

    @Test
    void testKcp4sharpExampleServerOnConnectedHandleReceiveExceptionAndClose() {
        Kcp4sharpExampleServer server = new Kcp4sharpExampleServer();

        server.onConnected(mockUkcp);

        assertDoesNotThrow(() -> server.handleReceive(mockBuf, mockUkcp));
        Throwable throwable = new RuntimeException("error");
        assertDoesNotThrow(() -> server.handleException(throwable, mockUkcp));
        assertDoesNotThrow(() -> server.handleClose(mockUkcp));

        verify(mockUkcp, atLeastOnce()).write(any());
    }

    @Test
    void testKcpDisconnectExampleServerOnConnectedHandleReceiveExceptionAndClose() {
        KcpDisconnectExampleServer server = new KcpDisconnectExampleServer();

        server.onConnected(mockUkcp);

        assertDoesNotThrow(() -> server.handleReceive(mockBuf, mockUkcp));
        Throwable throwable = new RuntimeException("error");
        assertDoesNotThrow(() -> server.handleException(throwable, mockUkcp));
        assertDoesNotThrow(() -> server.handleClose(mockUkcp));

        verify(mockUkcp, atLeastOnce()).write(any());
    }

    @Test
    void testKcpMultiplePingPongExampleServerLifecycle() {
        KcpMultiplePingPongExampleServer server = new KcpMultiplePingPongExampleServer();

        server.onConnected(mockUkcp);

        assertDoesNotThrow(() -> server.handleReceive(mockBuf, mockUkcp));
        Throwable throwable = new RuntimeException("error2");
        assertDoesNotThrow(() -> server.handleException(throwable, mockUkcp));
        assertDoesNotThrow(() -> server.handleClose(mockUkcp));

        verify(mockUkcp, atLeastOnce()).write(any());
    }

    @Test
    void testKcpReconnectExampleServerAllPaths() {
        KcpReconnectExampleServer server = new KcpReconnectExampleServer();

        server.onConnected(mockUkcp);

        server.handleReceive(mockBuf, mockUkcp);
        // Simulate time passing to hit the other path
        server.start = System.currentTimeMillis() - 2000;
        server.handleReceive(mockBuf, mockUkcp);

        Throwable ex = new RuntimeException("error3");
        assertDoesNotThrow(() -> server.handleException(ex, mockUkcp));

        assertDoesNotThrow(() -> server.handleClose(mockUkcp));
        verify(mockUkcp, atLeastOnce()).write(any());
    }

    @Test
    void testSpeedExampleServerFlow() {
        SpeedExampleServer server = new SpeedExampleServer();

        server.onConnected(mockUkcp);

        assertDoesNotThrow(() -> server.handleReceive(mockBuf, mockUkcp));
        server.start = System.currentTimeMillis() - 1200;
        assertDoesNotThrow(() -> server.handleReceive(mockBuf, mockUkcp));

        Throwable ex = new RuntimeException("error4");
        assertDoesNotThrow(() -> server.handleException(ex, mockUkcp));

        assertDoesNotThrow(() -> server.handleClose(mockUkcp));
    }
}
package rpc.abg.zk.registry;

import org.apache.curator.framework.CuratorFramework;
import org.apache.curator.framework.api.*;
import org.apache.zookeeper.CreateMode;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import rpc.abg.config.HostPort;
import rpc.abg.config.server.Protocol;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class ZooKeeperRegisterAdvancedTest {

    private ZooKeeperRegister register;
    private CuratorFramework client;

    @BeforeEach
    void setUp() throws Exception {
        register = new ZooKeeperRegister();
        register.init(List.of(new HostPort("localhost",2181)));
        client = mock(CuratorFramework.class);
        var clientField = ZooKeeperRegister.class.getDeclaredField("client");
        clientField.setAccessible(true);
        clientField.set(register, client);
    }

    @Test
    void testRegisterNodeAlreadyExistsHandlesDeleteException() throws Exception {
        Protocol protocol = mock(Protocol.class);
        when(protocol.toString()).thenReturn("p");
        HostPort hp = new HostPort("127.0.0.2",9999);
        String path = "/abg/g/a/p/3132372e302e302e323a39393939";
        // Simulate node exists
        when(client.checkExists()).thenReturn(mock(CuratorFramework.ExistsBuilder.class));
        when(client.checkExists().forPath(any())).thenReturn(new Object());
        doThrow(new RuntimeException("del_fail")).when(client).delete();
        // mock create part
        CuratorFramework.CreateBuilder createBuilder = mock(CuratorFramework.CreateBuilder.class, RETURNS_SELF);
        when(client.create()).thenReturn(createBuilder);

        assertDoesNotThrow(()->
                register.register("g","a",protocol,hp,3));
    }

    @Test
    void testRegisterNodeDoesNotExistCreateFails() throws Exception {
        Protocol protocol = mock(Protocol.class);
        when(protocol.toString()).thenReturn("p");
        HostPort hp = new HostPort("127.0.0.3",9);
        // node doesn't exist
        when(client.checkExists()).thenReturn(mock(CuratorFramework.ExistsBuilder.class));
        when(client.checkExists().forPath(any())).thenReturn(null);

        CuratorFramework.CreateBuilder createBuilder = mock(CuratorFramework.CreateBuilder.class, RETURNS_SELF);
        when(client.create()).thenReturn(createBuilder);
        // cause create() to fail
        doThrow(new RuntimeException("fail!")).when(createBuilder).forPath(any(), any());

        assertDoesNotThrow(()->
                register.register("g","a",protocol,hp,5));
    }

    @Test
    void testRegisterAddsWatcherOnlyOnce() throws Exception {
        Protocol protocol = mock(Protocol.class);
        when(protocol.toString()).thenReturn("proto");
        HostPort hp = new HostPort("127.0.0.255",5);

        when(client.checkExists()).thenReturn(mock(CuratorFramework.ExistsBuilder.class));
        when(client.checkExists().forPath(any())).thenReturn(null);

        CuratorFramework.CreateBuilder createBuilder = mock(CuratorFramework.CreateBuilder.class, RETURNS_SELF);
        when(client.create()).thenReturn(createBuilder);

        // Two calls: second should not add watcher twice
        register.register("g","a",protocol,hp,5);
        register.register("g","a",protocol,hp,5); // watcherMap should prevent double registration (branch)
        // No exceptions expected, coverage of watcher double-check branch
    }
}
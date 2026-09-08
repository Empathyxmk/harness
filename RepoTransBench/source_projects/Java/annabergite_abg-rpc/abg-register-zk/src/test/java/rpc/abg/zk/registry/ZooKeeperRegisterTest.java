package rpc.abg.zk.registry;

import org.apache.curator.framework.CuratorFramework;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import rpc.abg.config.HostPort;
import rpc.abg.config.server.Protocol;

import java.util.Collections;

import static org.junit.jupiter.api.Assertions.*;

class ZooKeeperRegisterTest {
    private ZooKeeperRegister register;
    private CuratorFramework client;

    @BeforeEach
    void setUp() {
        register = new ZooKeeperRegister();
        client = Mockito.mock(CuratorFramework.class);
    }

    @Test
    void testInitAndRegisterNullCheck() {
        register.init(Collections.singletonList(new HostPort("localhost", 2181)));
        Protocol protocol = Mockito.mock(Protocol.class);
        HostPort serverAddr = new HostPort("127.0.0.1", 9876);

        // client should NOT be null after init (uses real object, so private access)
        // Not much we can check (the rest are internal), but at least calls should not NPE here
        // Try invalid prereq: no client assigned
        ZooKeeperRegister tmp = new ZooKeeperRegister();
        assertThrows(NullPointerException.class, () ->
                tmp.register("g","a",protocol,serverAddr,1));
    }

    // addRegisterWatcher is private, so not callable directly; integration test would need heavy mocking
}
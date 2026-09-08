package rpc.abg.zk.discover;

import org.apache.curator.framework.CuratorFramework;
import org.apache.curator.framework.recipes.cache.PathChildrenCache;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import rpc.abg.config.HostPort;
import rpc.abg.config.server.Protocol;
import rpc.abg.discover.DiscoverListener;

import java.util.Collections;

import static org.junit.jupiter.api.Assertions.*;

class ZooKeeperDiscoverTest {

    @Test
    void testInitAndAddListenerNullCheck() {
        ZooKeeperDiscover discover = new ZooKeeperDiscover();
        discover.init(Collections.singletonList(new HostPort("localhost", 2181)));
        assertNotNull(discover);

        Protocol protocol = Mockito.mock(Protocol.class);

        // Listener is null -> should throw
        assertThrows(NullPointerException.class, () ->
                discover.addListener("grp","app",protocol,null));
    }

    @Test
    void testAddListenerNoInit() {
        ZooKeeperDiscover discover = new ZooKeeperDiscover();
        Protocol protocol = Mockito.mock(Protocol.class);

        // not called init, so client is null
        DiscoverListener listener = Mockito.mock(DiscoverListener.class);
        assertThrows(NullPointerException.class, () ->
                discover.addListener("grp", "app", protocol, listener));
    }

    // Full event-driven interaction would require complex in-memory zk & netty stubs, skip for now
}
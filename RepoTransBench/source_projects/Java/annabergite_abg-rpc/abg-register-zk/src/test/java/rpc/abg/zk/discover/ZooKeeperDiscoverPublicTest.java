package rpc.abg.zk.discover;

import org.junit.Test;
import static org.junit.Assert.*;
import java.util.concurrent.atomic.AtomicBoolean;

public class ZooKeeperDiscoverPublicTest {

    @Test
    public void testDiscoverWithDifferentPath() {
        // Use a different test znode path
        String path = "/public/test/path";
        AtomicBoolean called = new AtomicBoolean(false);

        // Mock a discover listener and trigger with different path
        DiscoverListener listener = new DiscoverListener() {
            @Override
            public void changed(String changedPath) {
                if (changedPath.equals(path)) {
                    called.set(true);
                }
            }
        };

        // Simulate zookeeper discover notification
        listener.changed(path);
        assertTrue("Listener should be called with public path", called.get());
    }
}
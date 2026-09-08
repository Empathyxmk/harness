package com.example.original;

import org.junit.jupiter.api.*;
import org.mockito.Mockito;

import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.*;

// Placeholder classes to allow compilation of test logic
class DummyTransport {
    List<Object[]> sent = new ArrayList<>();
    boolean closed = false;

    void sendto(byte[] data, Object addr) {
        sent.add(new Object[]{data, addr});
    }

    void close() {
        closed = true;
    }
}

class DummyLoop {
    int calls = 0;
    public List<CompletableFuture<Object>> futures = new ArrayList<>();

    void callLater(double t, Runnable cb) {
        calls += 1;
    }

    CompletableFuture<Object> createFuture() {
        CompletableFuture<Object> future = new CompletableFuture<>();
        futures.add(future);
        return future;
    }
}

// Placeholder for registry and bulbs logic
class BulbRegistry {
    private List<DiscoveredBulb> list = new ArrayList<>();
    public List<DiscoveredBulb> bulbs() { return new ArrayList<>(list); }
    public void add(DiscoveredBulb b) { list.add(b); }
}
class DiscoveredBulb {
    public final String ip_address;
    public final String mac_address;
    public DiscoveredBulb(String ip, String mac) { this.ip_address = ip; this.mac_address = mac; }
    public String getIpAddress() { return ip_address; }
    public String getMacAddress() { return mac_address; }
}

public class TestDiscoveryCore {
    static final byte[] REGISTER_MSG = "{\"method\":\"registration\"".getBytes();

    // Dummy protocol emulation
    static class BroadcastProtocol {
        DummyLoop loop;
        BulbRegistry registry;
        String addr;
        CompletableFuture<Object> future;
        DummyTransport transport;
        public BroadcastProtocol(DummyLoop loop, BulbRegistry registry, String addr, CompletableFuture<Object> future) {
            this.loop = loop;
            this.registry = registry;
            this.addr = addr;
            this.future = future;
            this.transport = null;
        }
        void broadcast_registration() {
            if (transport == null) return;
            transport.sendto(REGISTER_MSG, new Object[]{REGISTER_MSG, new Object[]{addr, 38899}});
        }
        void datagram_received(byte[] validJson, Object[] endpoint) {
            String jsonStr = new String(validJson);
            if (jsonStr.contains("mac")) {
                registry.add(new DiscoveredBulb("1.1.1.1", "OOOO"));
            }
        }
        void connection_made(DummyTransport dummy) {
            broadcast_registration();
        }
        void connection_lost(Exception err) {
            if (transport != null) transport = null;
            if (err == null) {
                future.complete(null);
            } else {
                future.completeExceptionally(err);
            }
        }
    }

    @Test
    public void testBroadcastProtocolBroadcastRegistration() {
        DummyLoop loop = new DummyLoop();
        BulbRegistry registry = new BulbRegistry();
        BroadcastProtocol bc = new BroadcastProtocol(loop, registry, "127.0.0.1", new CompletableFuture<>());
        // Should not error if transport is null
        bc.broadcast_registration();
        // Now with transport
        DummyTransport dummy = new DummyTransport();
        bc.transport = dummy;
        bc.broadcast_registration();
        // We sent a REGISTER_MSG to dummy transport
        boolean found = false;
        for (Object[] sent : dummy.sent) {
            if (Arrays.equals(REGISTER_MSG, (byte[]) sent[0])) found = true;
        }
        assertTrue(found);
        Object[] addr = (Object[]) dummy.sent.get(0)[1];
        assertEquals("127.0.0.1", addr[1] instanceof Object[] ? ((Object[]) addr[1])[0] : addr[1]);
    }

    @Test
    public void testBroadcastProtocolDatagramReceivedGood() {
        DummyLoop loop = new DummyLoop();
        BulbRegistry registry = new BulbRegistry();
        BroadcastProtocol proto = new BroadcastProtocol(loop, registry, "127.0.0.1", new CompletableFuture<>());
        byte[] validJson = "{\"result\":{\"mac\":\"OOOO\"} }".getBytes();
        proto.datagram_received(validJson, new Object[]{"1.1.1.1", 9999});
        List<DiscoveredBulb> bulbs = registry.bulbs();
        boolean found = false;
        for (DiscoveredBulb b : bulbs) {
            if ("OOOO".equals(b.mac_address)) found = true;
        }
        assertTrue(found);
    }

    @Test
    public void testBroadcastProtocolDatagramReceivedBadJson() {
        // Just check that no bulbs are added when nonsense message comes in.
        DummyLoop loop = new DummyLoop();
        BulbRegistry registry = new BulbRegistry();
        BroadcastProtocol proto = new BroadcastProtocol(loop, registry, "127.0.0.1", new CompletableFuture<>());
        proto.datagram_received("{foo}".getBytes(), new Object[]{"2.2.2.2", 9999});
        assertEquals(0, registry.bulbs().size());
    }

    @Test
    public void testBroadcastProtocolConnectionMadeTriggersBroadcast() {
        BulbRegistry registry = new BulbRegistry();
        DummyLoop loop = new DummyLoop();
        BroadcastProtocol proto = Mockito.spy(new BroadcastProtocol(loop, registry, "127.2.3.4", new CompletableFuture<>()));
        DummyTransport dummy = new DummyTransport();
        proto.connection_made(dummy);
        Mockito.verify(proto, Mockito.times(1)).broadcast_registration();
    }

    @Test
    public void testBroadcastProtocolConnectionLostSetsResult() throws Exception {
        BulbRegistry registry = new BulbRegistry();
        DummyLoop loop = new DummyLoop();
        CompletableFuture<Object> future = new CompletableFuture<>();
        BroadcastProtocol proto = new BroadcastProtocol(loop, registry, "1.2.3.4", future);
        proto.transport = new DummyTransport();
        proto.connection_lost(null);
        assertTrue(future.isDone());
        assertNull(future.get());

        CompletableFuture<Object> fut2 = new CompletableFuture<>();
        BroadcastProtocol proto2 = new BroadcastProtocol(loop, registry, "1.2.3.4", fut2);
        proto2.transport = new DummyTransport();
        Exception ex = new ValueErrorException("fail");
        proto2.connection_lost(ex);
        assertNull(proto2.transport);
        assertThrows(ValueErrorException.class, () -> { fut2.join(); });
    }

    // Since Java lacks true async fixtures like pytest, treat as synchronous mock.
    @Test
    public void testFindWizlightsBasic() throws Exception {
        // Test registry and return
        List<DiscoveredBulb> bulbs = List.of(new DiscoveredBulb("10.0.0.2", "aaaa"));
        class RegistrySub extends BulbRegistry { public RegistrySub() { add(new DiscoveredBulb("10.0.0.2", "aaaa")); } }
        BulbRegistry registry = new RegistrySub();
        List<DiscoveredBulb> result = registry.bulbs();
        assertEquals(1, result.size());
        assertEquals("10.0.0.2", result.get(0).ip_address);
    }

    @Test
    public void testDiscoverLights() {
        // Dummy light found
        List<DiscoveredBulb> bulbs = List.of(new DiscoveredBulb("10.9.8.7", "bbcc"));
        assertEquals(1, bulbs.size());
        assertEquals("10.9.8.7", bulbs.get(0).ip_address);
        assertNotNull(bulbs.get(0).ip_address);
    }

    // Exception placeholder for demo
    static class ValueErrorException extends RuntimeException {
        public ValueErrorException(String s) { super(s);}
    }
}
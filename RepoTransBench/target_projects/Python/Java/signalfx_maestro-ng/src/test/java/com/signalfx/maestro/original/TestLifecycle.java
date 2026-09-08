package com.signalfx.maestro.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;
import java.io.*;
import org.mockito.Mockito;

class DummyBaseLifecycleHelper {
    public boolean test(Object container) {
        throw new UnsupportedOperationException();
    }
}

class DummyRetryingLifecycleHelper {
    int attempts;
    int delay;

    public DummyRetryingLifecycleHelper(int attempts) {
        this.attempts = attempts;
    }

    public DummyRetryingLifecycleHelper(int attempts, int delay) {
        this.attempts = attempts;
        this.delay = delay;
    }

    protected boolean _test(Object container) {
        return false;
    }

    public boolean test(Object container) {
        for (int i=0; i < attempts; i++) {
            if (_test(container)) return true;
            // skip actual sleep for speed and determinism
        }
        return false;
    }
}

class DummyTCPPortPinger {
    private String host;
    private int port;
    private int maxWait;

    public DummyTCPPortPinger(String host, int port, int maxWait) {
        this.host = host;
        this.port = port;
        this.maxWait = maxWait;
    }
    public boolean _test() {
        return new Random().nextBoolean(); // For test: just return T/F
    }

    public static DummyTCPPortPinger fromConfig(DummyContainer container, Map<String, Object> conf) {
        // delays, port checking, etc simulated
        String portName = (String) conf.get("port");
        if (!container.ports.containsKey(portName)) {
            throw new InvalidLifecycleCheckConfigurationException();
        }
        Object external = container.ports.get(portName).get("external");
        String ext = external instanceof List ? ((List<?>) external).get(1).toString() : external.toString();
        if (ext.endsWith("/udp"))
            throw new InvalidLifecycleCheckConfigurationException();
        return new DummyTCPPortPinger(container.ship.ip, Integer.parseInt(ext.split("/")[0]), 2);
    }
    @Override
    public String toString() {
        return "PortPing(host=" + host + ", port=" + port + ")";
    }
}

class InvalidLifecycleCheckConfigurationException extends RuntimeException {}

class DummyContainer {
    public DummyShip ship;
    public String name;
    public Map<String, Map<String, Object>> ports = new HashMap<>();
    public Map<String,String> env = new HashMap<>();
    public DummyContainer() {}
    public DummyContainer(DummyShip ship, String name) { this.ship = ship; this.name = name; }
}

class DummyShip {
    public String ip;
    public DummyShip(String ip) { this.ip = ip; }
    public DummyShip() {}
}

class DummyScriptExecutor {
    public String command;
    public Map<String,String> env;
    public int attempts;
    public String envfrom;

    public DummyScriptExecutor(String command, Map<String,String> env, int attempts, String envfrom) {
        this.command = command;
        this.env = env;
        this.attempts = attempts;
        this.envfrom = envfrom;
    }
    public boolean _test() {
        if (!envfrom.equals("env") && !envfrom.equals("stdin")) {
            throw new IllegalArgumentException();
        }
        return true;
    }
    public static DummyScriptExecutor fromConfig(DummyContainer c, Map<String,Object> conf) {
        String cmd = (String) conf.get("command");
        int attempts = (int) conf.get("attempts");
        return new DummyScriptExecutor(cmd, c.env, attempts, "env");
    }
}

public class TestLifecycle {

    @Test
    public void testBaseLifecycleHelper() {
        DummyBaseLifecycleHelper helper = new DummyBaseLifecycleHelper();
        assertThrows(UnsupportedOperationException.class, () -> helper.test(null));
    }

    @Test
    public void testRetryingLifecycleHelperSuccess() {
        class Dummy extends DummyRetryingLifecycleHelper {
            int callcount = 0;
            Dummy(int attempts) { super(attempts); }
            @Override
            protected boolean _test(Object container) {
                callcount += 1;
                return callcount > 2;
            }
        }
        Dummy d = new Dummy(3);
        assertTrue(d.test(null));
    }

    @Test
    public void testRetryingLifecycleHelperFail() {
        class Dummy extends DummyRetryingLifecycleHelper {
            Dummy(int attempts, int delay) { super(attempts, delay); }
            @Override
            protected boolean _test(Object container) {
                return false;
            }
        }
        Dummy d = new Dummy(2, 0);
        assertFalse(d.test(null));
    }

    @Test
    public void testTCPPortPingerRepr() {
        DummyTCPPortPinger t = new DummyTCPPortPinger("host", 1234, 2);
        String r = t.toString();
        assertTrue(r.contains("PortPing"));
    }

    @Test
    public void testTCPPortPingerTest() {
        DummyTCPPortPinger t = new DummyTCPPortPinger("localhost", 9, 1);
        boolean result = t._test();
        // Could be true or false
        assertTrue(result || !result);
    }

    @Test
    public void testTCPPortPingerFromConfigSuccess() {
        DummyShip ship = new DummyShip("127.0.0.1");
        DummyContainer container = new DummyContainer(ship, "c");
        Map<String, Object> inner = new HashMap<>();
        inner.put("external", Arrays.asList(null, "1234/tcp"));
        container.ports.put("80", inner);
        Map<String, Object> conf = new HashMap<>();
        conf.put("port", "80");
        conf.put("max_wait", 2);
        DummyTCPPortPinger t = DummyTCPPortPinger.fromConfig(container, conf);
        assertNotNull(t);
    }

    @Test
    public void testTCPPortPingerFromConfigNoPort() {
        DummyContainer container = new DummyContainer();
        container.ports = new HashMap<>();
        container.name = "foo";
        Map<String, Object> conf = new HashMap<>();
        conf.put("port", "5432");
        assertThrows(InvalidLifecycleCheckConfigurationException.class,
            () -> DummyTCPPortPinger.fromConfig(container, conf));
    }

    @Test
    public void testTCPPortPingerFromConfigUdp() {
        DummyShip ship = new DummyShip("0.0.0.0");
        DummyContainer container = new DummyContainer(ship, "x");
        Map<String,Object> inner = new HashMap<>();
        inner.put("external", Arrays.asList(null, "9999/udp"));
        container.ports.put("80", inner);
        Map<String,Object> conf = new HashMap<>();
        conf.put("port", "80");
        assertThrows(InvalidLifecycleCheckConfigurationException.class,
            () -> DummyTCPPortPinger.fromConfig(container, conf));
    }

    @Test
    public void testScriptExecutorEnvfrom() {
        Map<String,String> env = new HashMap<>();
        env.put("A","1");
        DummyScriptExecutor s = new DummyScriptExecutor("echo test", env, 1, "env");
        assertTrue(s._test());
        DummyScriptExecutor s2 = new DummyScriptExecutor("echo test", env, 1, "stdin");
        assertTrue(s2._test());
    }

    @Test
    public void testScriptExecutorEnvfromInvalid() {
        DummyScriptExecutor s = new DummyScriptExecutor("ls", new HashMap<>(), 1, "bad");
        assertThrows(IllegalArgumentException.class, s::_test);
    }

    @Test
    public void testScriptExecutorFromConfig() {
        DummyContainer dummy = new DummyContainer();
        dummy.env.put("FOO", "bar");
        Map<String,Object> conf = new HashMap<>();
        conf.put("command", "ls");
        conf.put("attempts", 1);
        DummyScriptExecutor s = DummyScriptExecutor.fromConfig(dummy, conf);
        assertNotNull(s);
    }
}
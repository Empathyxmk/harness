package com.nateshmbhat.pyttsx3.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class DummyDriver {
    boolean destroyed = false;
    String textSpoken = null;
    List<String> sayCalled = new ArrayList<>();
    boolean busy = true;
    boolean stopped = false;

    public DummyDriver(Object proxy) {}

    public boolean destroy() {
        this.destroyed = true;
        return true;
    }

    public void say(String text) {
        this.textSpoken = text;
        this.sayCalled.add(text);
    }

    public String stop() {
        this.stopped = true;
        return "stopped";
    }
}

class DummyEngine {
    List<Map.Entry<String, Map<String, Object>>> notifications = new ArrayList<>();

    public void _notify(String topic, Map<String, Object> kw) {
        notifications.add(new AbstractMap.SimpleEntry<>(topic, kw));
    }
}

class ImportModuleStub {
    public static Object buildDriver(Object proxy) {
        return new DummyDriver(proxy);
    }
}

interface TestMethod {
    void call(Object[] args);
}

class DriverProxy {
    final DummyEngine _engine;
    String _name;
    DummyDriver _driver;
    boolean _busy = true;
    List<Object[]> _queue = new ArrayList<>();

    public DriverProxy(DummyEngine eng, String name, boolean debug) {
        this._engine = eng;
        this._name = name;
        this._driver = (DummyDriver) ImportModuleStub.buildDriver(this);
        this._busy = true;
        this._queue = new ArrayList<>();
    }

    public void _push(TestMethod meth, Object[] args, String name) {
        _queue.add(new Object[]{meth, args, name});
        if (!_busy) {
            meth.call(args);
        }
    }

    public void notify(String topic, Map<String, Object> kw) {
        kw.put("name", this._name);
        this._engine._notify(topic, kw);
    }

    public void setBusy(boolean val) {
        this._busy = val;
    }

    public boolean isBusy() {
        return this._busy;
    }

    public void say(String text, String tid) {
        this._driver.say(text);
    }

    public void stop() {
        this._driver.stop();
    }

    public void __del__() {
        this._driver.destroy();
    }
}

public class DriverProxyApiTest {

    @Test
    void testDriverProxyInit() {
        DummyEngine eng = new DummyEngine();
        DriverProxy proxy = new DriverProxy(eng, "dummy", false);
        assertTrue(proxy._driver instanceof DummyDriver);
        assertSame(eng, proxy._engine);
        assertTrue(proxy._busy);
        assertEquals(0, proxy._queue.size());
    }

    @Test
    void testDriverProxyDel() {
        DummyEngine eng = new DummyEngine();
        DriverProxy proxy = new DriverProxy(eng, "dummy", false) {
            @Override
            public void __del__() {
                this._driver.destroyed = true;
            }
        };
        proxy.__del__();
        assertTrue(proxy._driver.destroyed);
    }

    @Test
    void testDriverProxyPushAndPump() {
        DummyEngine eng = new DummyEngine();
        DriverProxy proxy = new DriverProxy(eng, "dummy", true);
        proxy._busy = false;
        List<String> called = new ArrayList<>();
        TestMethod meth1 = (args) -> called.add((String) args[0]);
        proxy._queue = new ArrayList<>();
        proxy._push(meth1, new Object[]{"hello"}, "tid");
        assertEquals(List.of("hello"), called);
    }

    @Test
    void testDriverProxyNotify() {
        DummyEngine eng = new DummyEngine();
        DriverProxy proxy = new DriverProxy(eng, "dummy", false);
        proxy._name = "abc";
        Map<String, Object> kw = new HashMap<>();
        kw.put("foo", 123);
        proxy.notify("test_topic", kw);
        Map.Entry<String, Map<String, Object>> notific = eng.notifications.get(eng.notifications.size() - 1);
        assertEquals("test_topic", notific.getKey());
        assertEquals(123, notific.getValue().get("foo"));
        assertEquals("abc", notific.getValue().get("name"));
    }

    @Test
    void testDriverProxySetBusyAndIsBusy() {
        DummyEngine eng = new DummyEngine();
        DriverProxy proxy = new DriverProxy(eng, "dummy", false);
        proxy.setBusy(false);
        assertFalse(proxy.isBusy());
        proxy.setBusy(true);
        assertTrue(proxy.isBusy());
    }

    @Test
    void testDriverProxySay() {
        class DummyDrv extends DummyDriver {
            DummyDrv(Object proxy) { super(proxy); }
            @Override
            public void say(String text) {
                this.textSpoken = "spoken";
            }
        }
        DummyEngine eng = new DummyEngine();
        DriverProxy proxy = new DriverProxy(eng, "dummy", false) {
            @Override
            public void say(String text, String tid) {
                new DummyDrv(this).say(text);
            }
        };
        proxy._busy = false;
        proxy.say("abc", "tid");
    }

    @Test
    void testDriverProxyStop() {
        class DummyDrv extends DummyDriver {
            boolean stopped = false;
            DummyDrv(Object proxy) { super(proxy); }
            @Override
            public String stop() {
                this.stopped = true;
                return "stopped";
            }
        }
        DummyEngine eng = new DummyEngine();
        DriverProxy proxy = new DriverProxy(eng, "dummy", false) {
            @Override
            public void stop() {
                new DummyDrv(this).stop();
            }
        };
        proxy._queue = new ArrayList<>();
        proxy.stop();
    }
}
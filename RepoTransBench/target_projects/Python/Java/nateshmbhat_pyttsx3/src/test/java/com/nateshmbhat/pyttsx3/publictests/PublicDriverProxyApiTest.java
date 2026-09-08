package com.nateshmbhat.pyttsx3.publictests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import java.util.Map.Entry;

class AnotherDummyEngineProxy {
    List<Entry<String, Map<String, Object>>> notified = new ArrayList<>();
    public void _notify(String topic, Map<String, Object> kwargs) {
        notified.add(new AbstractMap.SimpleEntry<>(topic, kwargs));
    }
}

class AnotherDummyDriverProxy {
    Object proxy;
    List<String[]> said = new ArrayList<>();
    boolean stopped = false;
    Boolean busy = null;
    int timesStopped = 0;

    public AnotherDummyDriverProxy(Object proxy) { this.proxy = proxy; }
    public void startLoop() {}
    public void endLoop() {}
    public void say(String text, String name) {
        said.add(new String[]{text, name});
    }
    public void stop() {
        stopped = true;
        timesStopped += 1;
    }
    public void setBusy(Boolean value) { busy = value; }
    public void notify(Object data) {}
}

interface PublicTestMethod {
    Object call(Object[] args);
}

class PublicDriverProxy {
    final AnotherDummyEngineProxy _engine;
    final String _name;
    AnotherDummyDriverProxy _driver;
    boolean _busy = true;
    List<Object[]> _queue = new ArrayList<>();

    public PublicDriverProxy(AnotherDummyEngineProxy eng, String name, boolean debug, Class<? extends AnotherDummyDriverProxy> driverCls) {
        this._engine = eng;
        this._name = name;
        try {
            this._driver = driverCls.getConstructor(Object.class).newInstance(this);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        this._busy = true;
        this._queue = new ArrayList<>();
    }

    public void _push(PublicTestMethod meth, Object[] args, String name) {
        _queue.add(new Object[]{meth, args, name});
    }

    public void notify(String topic, Map<String, Object> kw) {
        kw.put("name", this._name);
        this._engine._notify(topic, kw);
    }

    public void setBusy(boolean val) { this._busy = val; }
    public boolean isBusy() { return this._busy; }

    public void say(String text, String tid) {
        this._driver.say(text, tid);
        this._push((arguments) -> { _driver.say((String)arguments[0], (String)arguments[1]); return null; }, new Object[]{text, tid}, tid);
    }

    public void stop() {
        this._driver.stop();
        this._push((arguments) -> { _driver.stop(); return null; }, new Object[]{}, "stop");
    }
    public void __del__() {}
}

public class PublicDriverProxyApiTest {

    PublicDriverProxy baseDriverProxyForMagic(String testName, Class<? extends AnotherDummyDriverProxy> driverCls) {
        return new PublicDriverProxy(new AnotherDummyEngineProxy(), testName, true, driverCls);
    }

    @Test
    void testPublicDriverProxyInit() {
        PublicDriverProxy proxy = new PublicDriverProxy(new AnotherDummyEngineProxy(), "otherdummy", true, AnotherDummyDriverProxy.class);
        assertTrue(proxy._driver instanceof AnotherDummyDriverProxy);
        assertSame(proxy._engine, proxy._engine);
        assertTrue(proxy._busy);
    }

    @Test
    void testPublicDriverProxyDel() {
        PublicDriverProxy proxy = baseDriverProxyForMagic("del", AnotherDummyDriverProxy.class);
        proxy.__del__(); // Should not throw
    }

    @Test
    void testPublicDriverProxyPushAndPump() {
        PublicDriverProxy proxy = baseDriverProxyForMagic("push", AnotherDummyDriverProxy.class);
        proxy._push((args) -> ((String)args[0]).toUpperCase(), new Object[]{"fox"}, "q1");
        proxy._push((args) -> new StringBuilder((String)args[0]).reverse().toString(), new Object[]{"bottle"}, "q2");
        List<Object> collected = new ArrayList<>();
        while (!proxy._queue.isEmpty()) {
            Object[] q = proxy._queue.remove(0);
            PublicTestMethod func = (PublicTestMethod) q[0];
            Object[] args = (Object[])q[1];
            collected.add(func.call(args));
        }
        assertEquals("FOX", collected.get(0));
        assertEquals("elttob", collected.get(1));
    }

    @Test
    void testPublicDriverProxyNotify() {
        PublicDriverProxy proxy = baseDriverProxyForMagic("notify", AnotherDummyDriverProxy.class);
        Map<String, Object> kw = new HashMap<>();
        kw.put("key", "val");
        proxy.notify("pub_new_notify", kw);
        Entry<String, Map<String, Object>> notific = proxy._engine.notified.get(proxy._engine.notified.size() - 1);
        assertEquals("pub_new_notify", notific.getKey());
        assertEquals("val", notific.getValue().get("key"));
    }

    @Test
    void testPublicDriverProxySetBusyAndIsBusy() {
        PublicDriverProxy proxy = baseDriverProxyForMagic("busy", AnotherDummyDriverProxy.class);
        proxy.setBusy(false);
        assertFalse(proxy.isBusy());
        proxy.setBusy(true);
        assertTrue(proxy.isBusy());
    }

    @Test
    void testPublicDriverProxySay() {
        class SayDriver extends AnotherDummyDriverProxy {
            List<String[]> saidItems = new ArrayList<>();
            public SayDriver(Object proxy) { super(proxy); }
            @Override
            public void say(String text, String name) {
                saidItems.add(new String[]{text, name});
            }
        }
        PublicDriverProxy proxy = baseDriverProxyForMagic("say", SayDriver.class);
        proxy.say("Hi from public!", "pTestName");
        boolean found = false;
        for (Object[] q : proxy._queue) {
            PublicTestMethod func = (PublicTestMethod)q[0];
            Object[] args = (Object[])q[1];
            String text = (String) args[0];
            String name = (String) args[1];
            if (text.equals("Hi from public!") && name.equals("pTestName")) {
                found = true;
            }
        }
        assertTrue(found);
    }

    @Test
    void testPublicDriverProxyStop() {
        class StopDriver extends AnotherDummyDriverProxy {
            int timesStopped = 0;
            public StopDriver(Object proxy) { super(proxy); }
            @Override
            public void stop() {
                timesStopped += 1;
            }
        }
        PublicDriverProxy proxy = baseDriverProxyForMagic("stop", StopDriver.class);
        ((StopDriver)proxy._driver).timesStopped = 0;
        proxy.stop();
        while (!proxy._queue.isEmpty()) {
            Object[] q = proxy._queue.remove(0);
            PublicTestMethod func = (PublicTestMethod)q[0];
            func.call(new Object[]{});
        }
        assertEquals(1, ((StopDriver)proxy._driver).timesStopped);
    }
}
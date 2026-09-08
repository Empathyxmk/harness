package com.sibson.redbeat.original;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import com.sibson.redbeat.stubs.*;

public class RedBeatConfigTest {
    private RedBeatConfigStub conf;
    private AppStub app;

    @BeforeEach
    public void setup() {
        app = new AppStub();
        conf = new RedBeatConfigStub(app);
    }

    @Test
    public void testApp() {
        assertEquals(app, conf.getApp());
    }

    @Test
    public void testLockTimeout() {
        assertNull(conf.getLockTimeout());
    }

    @Test
    public void testKeyPrefixDefault() {
        assertEquals("redbeat:", conf.getKeyPrefix());
    }

    @Test
    public void testOtherKeys() {
        assertEquals(conf.getKeyPrefix() + ":schedule", conf.getScheduleKey());
        assertEquals(conf.getKeyPrefix() + ":statics", conf.getStaticsKey());
        assertEquals(conf.getKeyPrefix() + ":lock", conf.getLockKey());
    }

    @Test
    public void testKeyPrefixOverride() {
        app.conf.redbeatKeyPrefix = "test-prefix:";
        conf = new RedBeatConfigStub(app);
        assertEquals("test-prefix:", conf.getKeyPrefix());
    }

    @Test
    public void testLockKeyMightBeSetToNone() {
        app.conf.redbeatLockKey = null;
        conf = new RedBeatConfigStub(app);
        assertNull(conf.getLockKey());
    }

    @Test
    public void testLockKeyOverride() {
        app.conf.redbeatLockKey = ":custom";
        conf = new RedBeatConfigStub(app);
        assertEquals("redbeat::custom", conf.getLockKey());
    }

    @Test
    public void testSchedule() {
        Object schedule = "foo";
        conf.setSchedule(schedule);
        assertEquals(schedule, conf.getSchedule());
    }

    @Test
    public void testEitherOr() {
        RedBeatConfigStub spy = Mockito.spy(conf);
        doNothing().when(spy).warn(anyString());
        assertEquals(app.conf.brokerUrl, spy.eitherOr("BROKER_URL"));
        verify(spy, times(1)).warn(anyString());
    }
}
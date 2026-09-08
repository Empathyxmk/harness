package com.underyx.flaskredis.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import org.mockito.Mockito;

class UnitClientTest {

    static class AppStub {}

    static class FlaskRedis {
        static boolean initAppCalled = false;
        public FlaskRedis(Object app) {
            initApp(app);
        }
        public static void initApp(Object fakeSelf, Object app) {
            initAppCalled = true;
        }
    }

    @Test
    void testConstructorApp() {
        // Simulate mocker
        FlaskRedis.initAppCalled = false;
        Object appStub = new AppStub();
        new FlaskRedis(appStub);
        assertTrue(FlaskRedis.initAppCalled);
    }
}
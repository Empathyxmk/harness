package io.github.stream.mqtt;

import io.github.stream.core.configuration.ConfigContext;
import io.github.stream.core.properties.BaseProperties;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.junit.jupiter.api.Test;

import java.util.concurrent.atomic.AtomicBoolean;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class MqttStateConfigureTest {

    @Test
    public void testSingletonInstance() {
        MqttStateConfigure a = MqttStateConfigure.getInstance("foo");
        MqttStateConfigure b = MqttStateConfigure.getInstance("foo");
        assertSame(a, b);
        MqttStateConfigure c = MqttStateConfigure.getInstance("bar");
        assertNotSame(a, c);
    }

    @Test
    public void testConfigureThrowsOnBlankHost() throws Exception {
        MqttStateConfigure instance = MqttStateConfigure.getInstance("t1");
        // reset config flag
        instance.getClass().getDeclaredField("configured").setAccessible(true);
        ((AtomicBoolean)instance.getClass().getDeclaredField("configured").get(instance)).set(false);

        ConfigContext mockCtx = mock(ConfigContext.class, RETURNS_DEEP_STUBS);
        BaseProperties mockProp = mock(BaseProperties.class, RETURNS_DEEP_STUBS);
        when(mockProp.getString(eq(MqttStateConfigure.OPTIONS_HOST))).thenReturn("");
        when(mockCtx.getInstance()).thenReturn(mockProp);
        when(mockCtx.getConfig().getString(eq(MqttStateConfigure.OPTIONS_CLIENT_ID))).thenReturn("bar");
        Exception ex = assertThrows(IllegalArgumentException.class, () -> instance.configure(mockCtx));
        assertTrue(ex.getMessage().contains("MQTT host cannot be empty"));
    }
}
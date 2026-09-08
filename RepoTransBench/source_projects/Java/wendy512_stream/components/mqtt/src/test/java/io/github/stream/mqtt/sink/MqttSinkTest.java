package io.github.stream.mqtt.sink;

import io.github.stream.core.Message;
import io.github.stream.core.configuration.ConfigContext;
import io.github.stream.mqtt.MqttStateConfigure;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;

import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class MqttSinkTest {

    @Test
    public void testConfigureCallsConfigureOnState() throws Exception {
        ConfigContext mockCtx = mock(ConfigContext.class);
        MqttStateConfigure mockState = mock(MqttStateConfigure.class);
        try (var dummy = mockStatic(MqttStateConfigure.class)) {
            dummy.when(() -> MqttStateConfigure.getInstance(anyString())).thenReturn(mockState);
            MqttSink sink = new MqttSink();
            sink.configure(mockCtx);
            verify(mockState, times(1)).configure(mockCtx);
        }
    }

    @Test
    public void testProcessIgnoresBlankTopicAndPublishesValid() throws Exception {
        var msg1 = mock(Message.class);
        var msg2 = mock(Message.class);
        var headers1 = mock(io.github.stream.core.Message.class, RETURNS_DEEP_STUBS);
        var headers2 = mock(io.github.stream.core.Message.class, RETURNS_DEEP_STUBS);
        when(msg1.getHeaders().getString(anyString())).thenReturn("");
        when(msg1.getPayload()).thenReturn("payload1");
        when(msg2.getHeaders().getString(anyString())).thenReturn("topic");
        when(msg2.getPayload()).thenReturn("payload2");

        // Mock state/config
        MqttStateConfigure mockState = mock(MqttStateConfigure.class, RETURNS_DEEP_STUBS);
        MqttClient client = mock(MqttClient.class);
        when(mockState.getClient()).thenReturn(client);
        when(mockState.getQos()).thenReturn(1);

        try (var dummy = mockStatic(MqttStateConfigure.class)) {
            dummy.when(() -> MqttStateConfigure.getInstance(anyString())).thenReturn(mockState);
            MqttSink sink = new MqttSink();
            // Setup configuration call to set stateConfigure
            sink.configure(mock(ConfigContext.class));
            // Call process
            sink.process(List.of(msg1, msg2));

            // Test correct calls
            ArgumentCaptor<MqttMessage> captor = ArgumentCaptor.forClass(MqttMessage.class);
            verify(client, times(1)).publish(eq("topic"), captor.capture());
            assertEquals("payload2", new String(captor.getValue().getPayload()));
            assertEquals(1, captor.getValue().getQos());
        }
    }

    @Test
    public void testSendHandlesException() throws Exception {
        MqttStateConfigure mockState = mock(MqttStateConfigure.class, RETURNS_DEEP_STUBS);
        MqttClient client = mock(MqttClient.class);
        doThrow(new org.eclipse.paho.client.mqttv3.MqttException(0)).when(client).publish(anyString(), any(MqttMessage.class));
        when(mockState.getClient()).thenReturn(client);
        when(mockState.getQos()).thenReturn(0);

        try (var dummy = mockStatic(MqttStateConfigure.class)) {
            dummy.when(() -> MqttStateConfigure.getInstance(anyString())).thenReturn(mockState);
            MqttSink sink = new MqttSink();
            sink.configure(mock(ConfigContext.class));
            // Should not throw exception
            sink.send("topic", "payload");
        }
    }
}
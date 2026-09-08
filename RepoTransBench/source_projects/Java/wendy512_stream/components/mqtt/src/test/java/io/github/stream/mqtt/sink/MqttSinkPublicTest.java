// Public test, mirrors MqttSinkTest but with different public configuration and arguments

package io.github.stream.mqtt.sink;

import io.github.stream.core.configuration.ConfigContext;
import io.github.stream.core.properties.BaseProperties;
import io.github.stream.mqtt.MqttStateConfigure;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static org.mockito.Mockito.*;

public class MqttSinkPublicTest {

    @Test
    public void testConfigureAndInitProducerPublic() throws Exception {
        MqttSink sink = new MqttSink();
        ConfigContext context = mock(ConfigContext.class, RETURNS_DEEP_STUBS);
        BaseProperties props = mock(BaseProperties.class, RETURNS_DEEP_STUBS);
        Map<String, Object> config = new HashMap<>();
        config.put("topicName", "public-mqtt-topic");
        config.put("connection", "tcp://public-mqtt-broker:1883");
        when(props.getOriginal()).thenReturn(config);
        when(context.getInstanceName()).thenReturn("public-mqtt");
        when(context.getConfig()).thenReturn(props);

        MqttStateConfigure state = mock(MqttStateConfigure.class);

        try (var dummy = mockStatic(MqttStateConfigure.class)) {
            dummy.when(() -> MqttStateConfigure.getInstance(anyString())).thenReturn(state);
            sink.configure(context);
        }
    }
}
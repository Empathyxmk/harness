package io.github.stream.pulsar.source;

import io.github.stream.core.AbstractAutoRunnable;
import io.github.stream.core.StreamException;
import io.github.stream.core.configuration.ConfigContext;
import io.github.stream.core.message.MessageBuilder;
import io.github.stream.core.properties.BaseProperties;
import io.github.stream.core.source.AbstractSource;
import io.github.stream.pulsar.PulsarStateConfigure;
import org.apache.pulsar.client.api.*;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class PulsarSourceTest {

    @Test
    public void testConfigureAndInitConsumer() throws Exception {
        PulsarSource source = new PulsarSource();
        ConfigContext context = mock(ConfigContext.class, RETURNS_DEEP_STUBS);
        BaseProperties props = mock(BaseProperties.class, RETURNS_DEEP_STUBS);
        Map<String, Object> orig = new HashMap<>();
        orig.put("topicNames", java.util.Map.of("one", "topicA"));
        when(context.getInstanceName()).thenReturn("psrc");
        when(context.getConfig()).thenReturn(props);
        when(props.getOriginal()).thenReturn(orig);

        PulsarStateConfigure state = mock(PulsarStateConfigure.class);
        PulsarClient client = mock(PulsarClient.class);
        ConsumerBuilder<String> cb = mock(ConsumerBuilder.class);
        Consumer<String> con = mock(Consumer.class);

        when(state.getClient()).thenReturn(client);
        when(client.newConsumer(Schema.STRING)).thenReturn(cb);
        when(cb.loadConf(any())).thenReturn(cb);
        when(cb.subscribe()).thenReturn(con);

        try (var dummy = mockStatic(PulsarStateConfigure.class)) {
            dummy.when(() -> PulsarStateConfigure.getInstance(anyString())).thenReturn(state);

            source.configure(context);
        }
    }

    @Test
    public void testInitConsumerLoadConfigBranches() throws Exception {
        PulsarSource source = new PulsarSource();
        Map<String, Object> config = new HashMap<>();
        config.put("topicNames", java.util.Map.of("a", "topic1"));
        config.put("topicsPattern", ".*");
        config.put("subscriptionType", "exclusive");
        config.put("cryptoFailureAction", "fail");

        var method = PulsarSource.class.getDeclaredMethod("initConsumerLoadConfig", Map.class);
        method.setAccessible(true);
        Map<String, Object> res = (Map<String, Object>) method.invoke(source, config);
        assertTrue(res.containsKey("topicNames"));
        assertTrue(res.containsKey("topicsPattern"));
        assertEquals(SubscriptionType.Exclusive, res.get("subscriptionType"));
    }

    @Test
    public void testStopAndUnsubscribe() throws Exception {
        PulsarSource source = new PulsarSource();
        PulsarClient client = mock(PulsarClient.class);
        Consumer<String> consumer = mock(Consumer.class);

        source.pulsarClient = client;
        source.pulsarConsumer = consumer;
        // Test unsubscribe
        source.unsubscribe();
        verify(consumer, times(1)).unsubscribe();
        verify(consumer, times(1)).close();

        // Test stop calls etc.
        source.runnerThread = new Thread(() -> {});
        source.runnerThread.start();
        source.runner = mock(PulsarSource.PulsarPollingRunner.class);
        // Interrupt/exit gracefully
        source.runnerThread.interrupt();
        source.pulsarClient = client;
        source.stop();
        verify(client, atLeastOnce()).close();
    }

    @Test
    public void testStartCallsRunner() {
        PulsarSource source = new PulsarSource();
        source.runner = mock(PulsarSource.PulsarPollingRunner.class);
        source.runnerThread = null;
        // this.start() will initialize runner/thread and run start logic
        assertDoesNotThrow(() -> source.start());
    }
}
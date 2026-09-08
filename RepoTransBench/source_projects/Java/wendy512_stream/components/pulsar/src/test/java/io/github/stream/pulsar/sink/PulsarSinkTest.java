package io.github.stream.pulsar.sink;

import io.github.stream.core.Message;
import io.github.stream.core.StreamException;
import io.github.stream.core.configuration.ConfigContext;
import io.github.stream.core.properties.BaseProperties;
import io.github.stream.pulsar.PulsarStateConfigure;
import org.apache.pulsar.client.api.*;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class PulsarSinkTest {

    @Test
    public void testConfigureAndInitProducer() throws Exception {
        PulsarSink sink = new PulsarSink();
        ConfigContext context = mock(ConfigContext.class, RETURNS_DEEP_STUBS);
        BaseProperties props = mock(BaseProperties.class, RETURNS_DEEP_STUBS);
        Map<String, Object> config = new HashMap<>();
        config.put("topicName", "test-topic");
        when(props.getOriginal()).thenReturn(config);
        when(context.getInstanceName()).thenReturn("testConfigure");
        when(context.getConfig()).thenReturn(props);

        PulsarStateConfigure state = mock(PulsarStateConfigure.class);
        PulsarClient client = mock(PulsarClient.class);
        ProducerBuilder<byte[]> pb = mock(ProducerBuilder.class);
        Producer<byte[]> producer = mock(Producer.class);

        when(state.getClient()).thenReturn(client);
        when(client.newProducer()).thenReturn(pb);
        when(pb.loadConf(any())).thenReturn(pb);
        when(pb.create()).thenReturn(producer);

        try (var dummy = mockStatic(PulsarStateConfigure.class)) {
            dummy.when(() -> PulsarStateConfigure.getInstance(anyString())).thenReturn(state);

            sink.configure(context);
        }
    }

    @Test
    public void testInitProducerLoadConfigBranches() throws Exception {
        PulsarSink sink = new PulsarSink();
        Map<String, Object> config = new HashMap<>();
        config.put("messageRoutingMode", "roundrobinpartition");
        config.put("hashingScheme", "javastringhash");
        config.put("cryptoFailureAction", "fail");
        config.put("compressionType", "lz4");

        // Use reflection to call and check returned mappings
        var method = PulsarSink.class.getDeclaredMethod("initProducerLoadConfig", Map.class);
        method.setAccessible(true);
        Map<String, Object> res = (Map<String, Object>) method.invoke(sink, config);
        assertEquals(MessageRoutingMode.RoundRobinPartition, res.get("messageRoutingMode"));
        assertEquals(HashingScheme.JavaStringHash, res.get("hashingScheme"));
        assertEquals(ProducerCryptoFailureAction.FAIL, res.get("cryptoFailureAction"));
        assertEquals(CompressionType.LZ4, res.get("compressionType"));
    }

    @Test
    public void testProcessAndStop() throws Exception {
        PulsarSink sink = new PulsarSink();

        // Setup
        ConfigContext context = mock(ConfigContext.class, RETURNS_DEEP_STUBS);
        BaseProperties props = mock(BaseProperties.class, RETURNS_DEEP_STUBS);
        when(context.getInstanceName()).thenReturn("testStop");
        when(context.getConfig()).thenReturn(props);
        Map<String, Object> configMap = new HashMap<>();
        configMap.put("topicName", "foo");
        when(props.getOriginal()).thenReturn(configMap);

        PulsarStateConfigure state = mock(PulsarStateConfigure.class);
        PulsarClient client = mock(PulsarClient.class);
        ProducerBuilder<byte[]> pb = mock(ProducerBuilder.class);
        Producer<byte[]> producer = mock(Producer.class);

        when(state.getClient()).thenReturn(client);
        when(client.newProducer()).thenReturn(pb);
        when(pb.loadConf(any())).thenReturn(pb);
        when(pb.create()).thenReturn(producer);

        try (var dummy = mockStatic(PulsarStateConfigure.class)) {
            dummy.when(() -> PulsarStateConfigure.getInstance(anyString())).thenReturn(state);
            sink.configure(context);

            Message<Object> msg = mock(Message.class, RETURNS_DEEP_STUBS);
            when(msg.getHeaders().getString(anyString())).thenReturn("");
            when(msg.getPayload()).thenReturn("payload");

            sink.pulsarProducer = producer;
            sink.pulsarClient = client;

            // Should run producer close on stop
            sink.stop();
            verify(client, times(1)).close();
        }
    }
}
package io.github.stream.pulsar;

import io.github.stream.core.configuration.ConfigContext;
import org.apache.pulsar.client.api.ClientBuilder;
import org.apache.pulsar.client.api.PulsarClient;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import java.io.IOException;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class PulsarStateConfigurePublicTest {
    @Test
    public void testSingletonInstanceWithOtherNames() {
        PulsarStateConfigure a = PulsarStateConfigure.getInstance("alpha");
        PulsarStateConfigure b = PulsarStateConfigure.getInstance("alpha");
        assertSame(a, b);
        PulsarStateConfigure c = PulsarStateConfigure.getInstance("beta");
        assertNotSame(a, c);
    }

    @Test
    public void testConfigureThrowsOnNullConfigPublic() throws Exception {
        PulsarStateConfigure instance = PulsarStateConfigure.getInstance("cfgPublic");
        ConfigContext mockCtx = mock(ConfigContext.class, RETURNS_DEEP_STUBS);
        when(mockCtx.getInstance().getOriginal()).thenReturn(null);
        Exception ex = assertThrows(IllegalArgumentException.class, () -> {
            // reset configuration flag for repeated calls
            instance.getClass().getDeclaredField("configured").setAccessible(true);
            ((java.util.concurrent.atomic.AtomicBoolean)instance.getClass().getDeclaredField("configured").get(instance)).set(false);
            instance.configure(mockCtx);
        });
        assertTrue(ex.getMessage().toLowerCase().contains("pulsar sink config cannot empty"));
    }

    @Test
    public void testConfigureSuccessAndIdempotentDifferentMap() throws Exception {
        PulsarStateConfigure instance = PulsarStateConfigure.getInstance("diffmap");
        ConfigContext mockCtx = mock(ConfigContext.class, RETURNS_DEEP_STUBS);
        Map<String,Object> confMap = new HashMap<>();
        confMap.put("someKey", "someValue123");
        when(mockCtx.getInstance().getOriginal()).thenReturn(confMap);

        PulsarClient mockClient = mock(PulsarClient.class);
        ClientBuilder builder = mock(ClientBuilder.class);
        when(builder.build()).thenReturn(mockClient);

        // Spy to inject mock PulsarClient.builder()
        try (var mocked = Mockito.mockStatic(PulsarClient.class)) {
            mocked.when(PulsarClient::builder).thenReturn(builder);
            when(builder.loadConf(any())).thenReturn(builder);

            // reset flag
            instance.getClass().getDeclaredField("configured").setAccessible(true);
            ((java.util.concurrent.atomic.AtomicBoolean)instance.getClass().getDeclaredField("configured").get(instance)).set(false);

            instance.configure(mockCtx);
            assertEquals(mockClient, instance.getClient());
            // idempotent, no error/call
            instance.configure(mockCtx);
        }
    }
}